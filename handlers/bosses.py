from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup

from config import dp, bot, db
import handlers.stop_lists as sl
import handlers.auxiliary_functions as af
from handlers import send_table


def boss_menu():
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="⛔️СТОП-ЛИСТ", callback_data="boss_stop_list")
    btn2 = InlineKeyboardButton(text="📝ОФИЦИАНТЫ", callback_data="boss_waiters_stat")
    btn3 = InlineKeyboardButton(text="📶РЕКЛАМА", callback_data="boss_commercial")
    btn4 = InlineKeyboardButton(text="ТАБЛИЦА", callback_data="boss_table")
    menu.add(btn1)
    menu.add(btn2)
    menu.add(btn3)
    menu.add(btn4)
    return menu


@dp.callback_query_handler(lambda call: call.data == "boss_commercial")
async def boss_commercial(call: types.CallbackQuery):
    await call.answer()
    try:
        boss_id = call.from_user.id
        total_click_count, current_click_count, total_guests_count, current_guests_count = af.total_and_current_counter()
        if total_click_count is None:
            total_click_count = 0
        text = (f"📈 <b>Статистика вовлеченности пользователей к заведению:</b>\n\n"
                f"▶️ <i>Кликабельность заведения через поиск:</i> <b>{total_click_count} ({current_click_count})</b>\n\n"
                f"✅ <i>Обслужено гостей через f2m:</i> <b>{total_guests_count} ({current_guests_count})</b>\n"
                "<blockquote>В скобках статистика за смену с 00:00 до 23:59</blockquote>")

        messag_obj = await bot.edit_message_text(chat_id=boss_id,
                                                 message_id=call.message.message_id,
                                                 text=text,
                                                 reply_markup=InlineKeyboardMarkup().row(
                                                     InlineKeyboardButton(text="⬅️ Назад",
                                                                          callback_data="back_to_boss_menu")))
        db.set_temp_users_message_id(boss_id, messag_obj.message_id)
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == "boss_waiters_stat")
async def boss_waiters_stat(call: types.CallbackQuery):
    await call.answer()
    try:
        boss_id = call.from_user.id
        stats = db.get_waiters_names_and_stats()
        text = "🗒 <b>Общая статистика по официантам:</b>\n\n"
        for waiter in stats:
            if None not in waiter:
                current_waiter_count = db.get_current_waiter_guests(waiter[0])
                current_waiter_earning = db.get_current_waiter_sells(waiter[0])
                text += (
                    f"⏺️ <i>{waiter[1]} {waiter[2]} {waiter[3]}</i>\n- Количество заказов: <b>{len(set(eval(waiter[4])))}"
                    f"({current_waiter_count})</b>\n- Выручка: <b>{waiter[5]}({current_waiter_earning})</b>\n\n")
            else:
                print("У официанта есть поля None в базе данных: ", waiter)
        text += "<blockquote>В скобках статистика за смену с 00:00 до 23:59</blockquote>"
        message_obj = await bot.edit_message_text(chat_id=boss_id,
                                                  message_id=call.message.message_id,
                                                  text=text,
                                                  reply_markup=InlineKeyboardMarkup().row(
                                                      InlineKeyboardButton(text="⬅️ Назад",
                                                                           callback_data="back_to_boss_menu")))
        db.set_temp_users_message_id(boss_id, message_obj.message_id)
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == "boss_stop_list")
async def boss_stop_list(call: types.CallbackQuery):
    await call.answer()
    boss_id = call.from_user.id
    if not db.check_stop_list_exists():
        db.create_stop_list()
    await sl.set_stop_list(boss_id, "boss", call.message.message_id)


@dp.callback_query_handler(lambda call: call.data == "back_to_boss_menu")
async def back_to_boss_menu(call: types.CallbackQuery):
    await call.answer()
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    except:
        print('Нет сообщения')
    await generate_boss_menu(call.from_user.id, None)


async def generate_boss_menu(boss_id, message_id=None):
    mes = db.get_users_temp_message_id(boss_id)
    text = ("<b>Привет!</b> 👋\n\n"
            f"*️⃣ Это панель управления <b>для менеджера</b> заведения <b>KoreanChick</b>\n\n"
            "<b><i>/СТОП-ЛИСТ</i></b> - добавление блюд в стоп-лист\n"
            "<b><i>/ОФИЦИАНТЫ</i></b> - статистика по работе официантов\n"
            "<b><i>/РЕКЛАМА</i></b> - статистика вовлеченности пользователей\n"
            "<b><i>/ТАБЛИЦА</i></b> - полный отчет о пользователях")
    if message_id:
        message_obj = await bot.edit_message_text(chat_id=boss_id,
                                                  message_id=mes[0],
                                                  text=text,
                                                  reply_markup=boss_menu())
    else:
        message_obj = await bot.send_message(
            chat_id=boss_id,
            text=text,
            reply_markup=boss_menu()
        )
    db.set_temp_users_message_id(boss_id, message_obj.message_id)


@dp.callback_query_handler(lambda call: call.data == "boss_table")
async def table(call: types.CallbackQuery):
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await send_table.send_table(call.message)
