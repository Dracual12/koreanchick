import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import dp, bot, db
from aiogram import types
import naim.normal as normal
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from naim.start_bot import buttons_start_02
from handlers import bosses
from menu import sort_the
import handlers.auxiliary_functions as af
from files.icons import icons
from waiters import waiter_start as w_start


@dp.message_handler(lambda message: message.text is not None and not message.text.startswith('/'))
async def handle_messages(message: types.Message):
    user = message.from_user.id
    # Получаем состояние пользователя из БД
    user_state = db.get_temp_users_state(message.from_user.id)
    if user_state == 'dont_like_to_eat':
        # Обрабатываем ввод продуктов, которые не ест пользователь
        products = normal.normal_list(message.text)
        text = "<b>Эти продукты ты не употребляешь в пищу:</b>\n"
        text += (f"<code>{products}</code>\n"
                 "\n"
                 "Всё верно?")
        db.set_temp_users_dont_like_to_eat(user, products)
        # Логируем нелюбимые продукты в сессии
        db.update_logging_session_dislike(str(user), products)
        await bot.delete_message(chat_id=user, message_id=message.message_id)
        await bot.edit_message_text(chat_id=user, message_id=db.get_users_temp_message_id(user)[0], text=text, reply_markup=create_confirmation_buttons())
    elif user_state == 'like_to_eat':
        products = normal.normal_list(message.text)
        text = "<b>Эти продукты ты предпочитаешь:</b>\n"
        text += (f"<code>{products}</code>\n"
                 "\n"
                 "Всё верно?")
        db.set_temp_users_like_to_eat(user, products)
        # Логируем любимые продукты в сессии
        db.update_logging_session_like(str(user), products)
        await bot.delete_message(chat_id=user, message_id=message.message_id)
        await bot.edit_message_text(chat_id=user, message_id=db.get_users_temp_message_id(user)[0], text=text,
                                    reply_markup=create_confirmation_buttons2())
    elif user_state == 'boss':
        if message.text == '123456':
            await bot.delete_message(chat_id=user, message_id=db.get_users_temp_message_id(user)[0])
            await bot.delete_message(chat_id=user, message_id=message.message_id)
            await bosses.generate_boss_menu(user)
        else:
            await bot.delete_message(user, message_id=message.message_id)
            try:
                await bot.edit_message_text(chat_id=user, message_id=db.get_users_temp_message_id(user)[0], text='Неверный пароль, введите еще раз:')
            except Exception as e:
                print(e)

    elif user_state == 'review':
        dish = message.text
        await bot.delete_message(chat_id=user, message_id=message.message_id)
        dish_id = db.restaurants_get_dish(dish)[0]
        db.set_temp_users_dish_id(user, dish_id)
        await choose_dish(dish_id, message)

    elif user_state == 'review_end':
        user_first_name = db.get_users_user_first_name(user)
        await bot.delete_message(chat_id=user, message_id=message.message_id)
        await bot.edit_message_text(chat_id=user,
                                    message_id=db.get_users_temp_message_id(user)[0],
                                    text=f"<b>Спасибо за отзыв! 🤜🤛</b>",
                                    reply_markup=buttons_02()
                                    )
    elif user_state == 'waiter_password' and message.text == '123456':
        idd = db.get_users_temp_message_id(user)[0]
        await bot.delete_message(user, message.message_id)
        message_obj = await bot.edit_message_text(
            chat_id=user,
            message_id=idd,
            text="Пожалуйста, введи свое ФИО в формате: "
                 "Иванов Иван Иванович"
        )
        db.set_temp_users_state(user, 'waiter_reg')
        db.set_temp_users_message_id(user, message_obj.message_id)

    elif user_state == 'waiter_reg':
        await w_start.start(message)
    elif user_state == 'get_order':
        if '»' not in message.text:
            try:
                remark = message.text
                client_id = eval(db.get_waiter_score(user))[-1]
                await bot.delete_message(chat_id=user, message_id=message.message_id)
                await w_start.save_remark(user, client_id, remark)
                await w_start.set_order(user, client_id)

            except Exception as e:
                print("remark error: ", e)
        else:
            dish = message.text
            await bot.delete_message(chat_id=user, message_id=message.message_id)
            dish_id = db.restaurants_get_dish(dish)[0]
            await w_start.dish_added(user, dish_id)

    elif user_state == 'order_table':
        await bot.delete_message(chat_id=user, message_id=message.message_id)
        await w_start.order_accepted(user, eval(db.get_waiter_score(user))[-1], message.text)
    else:
        print("Состояние не определено, пропускаем")


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    phone = message.contact.phone_number
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=db.get_users_temp_message_id(message.from_user.id)[0])
    db.set_users_phone(message.from_user.id, phone)
    # Логируем телефон в сессии
    db.update_logging_session_phone(str(message.from_user.id), phone)
    mes = await message.answer("Одну секунду... ⏳", reply_markup=types.ReplyKeyboardRemove())
    await bot.delete_message(chat_id=message.from_user.id, message_id=mes.message_id)
    await message.answer(text="Спасибо! Теперь вы можете продолжить оформление заказа.", reply_markup=create_web_app_button())

@dp.message_handler(commands=['waiter'])
async def waiter(message: types.Message):
    user = message.from_user.id
    await bot.delete_message(user, message.message_id)
    if not db.check_waiter_exists(user):
        message_obj = await bot.send_message(
            chat_id=user,
            text="Введите пароль: ",
        )
        db.set_temp_users_state(user, 'waiter_password')
        db.set_temp_users_message_id(user, message_obj.message_id)
    else:
        text = f'\nТы уже зарегистрировался(ась) как официант'
        await bot.send_message(user, text)


@dp.message_handler(commands=['kbzhu'])
async def kbzhu(message: types.Message):
    user = message.from_user.id
    message = message.message_id
    mes = db.get_users_temp_message_id(user)
    await bot.delete_message(chat_id=user, message_id=message)
    try:
        await bot.delete_message(chat_id=user, message_id=mes[0])
    except Exception as e:
        print(e)
    dish, length, numb = sort_the.get_dish(user)
    kb = dish['КБЖУ']

    try:
        message_obj = await bot.send_message(user,
                                                 f"📝КБЖУ блюда :\n <tg-spoiler><i>{kb}</i></tg-spoiler>\n",
                                                 reply_markup=return_after_dish_info())
    except:
        message_obj = await bot.send_message(user,
                                             f"📝Мы пока не обладаем информацией о КБЖУ данного блюда\n",
                                             reply_markup=return_after_dish_info())
    db.set_temp_users_message_id(user, message_obj.message_id)


@dp.message_handler(commands=['com'])
async def com(message: types.Message):
    user = message.from_user.id
    message = message.message_id
    mes = db.get_users_temp_message_id(user)
    await bot.delete_message(chat_id=user, message_id=message)
    await bot.delete_message(chat_id=user, message_id=mes[0])
    dish, length, numb = sort_the.get_dish(user)
    if dish['Описание']:
        message_obj = await bot.send_message(user,
                                             f"<blockquote><i>👨🏼‍⚕️: {dish['Описание'].split(';')[0]}</i></blockquote>\n\n",
                                             reply_markup=return_after_dish_info())
    else:
        message_obj = await bot.send_message(user,
                                             f"<blockquote><i>👨🏼‍⚕️: {dish['Описание']}</i></blockquote>\n\n",
                                             reply_markup=return_after_dish_info())
    db.set_temp_users_message_id(user, message_obj.message_id)



@dp.message_handler(commands=['sostav'])
async def com(message: types.Message):
    user = message.from_user.id
    message = message.message_id
    mes = db.get_users_temp_message_id(user)
    await bot.delete_message(chat_id=user, message_id=message)
    try:
        await bot.delete_message(chat_id=user, message_id=mes[0])
    except Exception as e:
        print(e)
    dish, length, numb = sort_the.get_dish(user)

    if dish['Ингредиенты'] is not None:
        message_obj = await bot.send_message(user,
                                             text=f"📝Состав блюда :\n <i>{', '.join(dish['Ингредиенты']).capitalize()}</i>\n",
                                             reply_markup=return_after_dish_info())
    else:
        message_obj = await bot.send_message(user,
                                             text=f"📝Состав блюда :\n <i>{str(db.get_dish_simple_sostav(dish['Ресторан'], dish['Название'])).capitalize()}</i>\n",
                                             reply_markup=return_after_dish_info())
    db.set_temp_users_message_id(user, message_obj.message_id)


def return_after_dish_info():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="return_to_dishes"))


@dp.callback_query_handler(text_contains=f"return_to_dishes")
async def return_to_dishes(call: types.CallbackQuery):
    user = call.from_user.id
    await call.answer()
    dish, length, numb = sort_the.get_dish(user)
    dish_id = db.get_temp_users_dish_id(user)
    size_list = dish['Размер']
    photo_dir = '/Users/artemijpetrov/PycharmProjects/koreanchickdouble/chick'

    all_files = {os.path.splitext(file)[0]: os.path.join(photo_dir, file) for file in os.listdir(photo_dir)}
    shemodi_dish_photo = False
    photo_shemodi = ''
    for j in all_files:
        if j in dish['Название'] or dish['Название'] in j:
            shemodi_dish_photo = True
            photo_shemodi = j
    if size_list:
        size_list = eval(size_list)
    if db.check_basket_exists(user):
        basket = eval(db.get_basket(user))
        if dish['Название'] in basket:
            in_basket = True
            quantity = basket[dish['Название']][1]
        else:
            in_basket = False
            quantity = 0
    else:
        in_basket = False
        quantity = 0
    if shemodi_dish_photo or (dish['Название'] in all_files and dish['Ресторан'] == 'Молодёжь'):
        if shemodi_dish_photo:
            file_path = all_files[photo_shemodi]
        else:
            file_path = all_files[dish['Название']]
        if os.path.isfile(file_path):
            await bot.delete_message(chat_id=user, message_id=call.message.message_id)
            text = af.generate_dish_text(user, icons, dish, length, numb, dish_id)
            message_obj = await bot.send_photo(user, open(file_path, 'rb'),
                                               caption=text,
                                               reply_markup=buttons_food_05(dish_id,
                                                                          db.get_client_temp_dish(user),
                                                                            length, numb, in_basket,
                                                                            bool(db.get_qr_scanned(user)), quantity,
                                                                            size_list, user))
            db.set_temp_users_message_id(user, message_obj.message_id)

# ======================================================================================================================
# ===== Создание клавиатур =================================================================================================
# ======================================================================================================================

def create_confirmation_buttons():
    menu = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text="Да, всё верно 👍🏻",
                                callback_data="blacklist_yes")

    btn2 = InlineKeyboardButton(text="Нет! Перепишу 👎🏻",
                                callback_data="blacklist_no")

    menu.row(btn1, btn2)

    return menu


def create_confirmation_buttons2():
    menu = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text="Да, всё верно 👍🏻",
                                callback_data="whitelist_yes")

    btn2 = InlineKeyboardButton(text="Нет! Перепишу 👎🏻",
                                callback_data="whitelist_no")

    menu.row(btn1, btn2)

    return menu


def create_web_app_button():
    webapp_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    webapp_keyboard.add(
        KeyboardButton(
            text="Открыть WebApp",
            url='http://t.me/koreanchickbot/F2M'
        )
    )
    return webapp_keyboard


async def choose_dish(dish_id, message: types.Message):
    user = message.from_user.id
    if db.get_users_ban(user):
        return None

    # Действие:
    dish = db.restaurants_get_by_id(dish_id)

    message_obj = await bot.edit_message_text(
        chat_id=user,
        message_id=db.get_users_temp_message_id(user)[0],
        text=f"💫 Блюдо:\n"
             f"<i>«{dish[2]}»</i>\n"
             f"\n"
             f"Оцените блюдо по шкале от 1 до 5 👇🏻",
        reply_markup=buttons_04(dish_id)
    )


def buttons_04(dish_id):
    menu = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(text="1 ⭐",
                                callback_data=f"review_stat_1_{dish_id}")

    btn2 = InlineKeyboardButton(text="2 ⭐",
                                callback_data=f"review_stat_2_{dish_id}")

    btn3 = InlineKeyboardButton(text="3 ⭐",
                                callback_data=f"review_stat_3_{dish_id}")

    btn4 = InlineKeyboardButton(text="4 ⭐",
                                callback_data=f"review_stat_4_{dish_id}")

    btn5 = InlineKeyboardButton(text="5 ⭐",
                                callback_data=f"review_stat_5_{dish_id}")

    menu.row(btn1, btn2, btn3, btn4, btn5)

    return menu


@dp.callback_query_handler(text_contains="review_stat")
async def review_star(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id
    data = call.data.split('_')
    rating = data[-2]
    # await dp.storage.set_data(user=user, data={'rating': rating})

    if db.get_users_ban(user):
        return None

        # Действие:
    dish_id = int(data[-1])
    dish = db.restaurants_get_by_id(dish_id)
    db.restaurants_set_rating(dish_id, int(data[-2]))

    # Сохраняем оценку в таблицу correlation_coefficients
    db.save_dish_rating(user, dish_id, int(data[-2]))

    await dp.storage.set_data(user=user, data={
        'rating': rating,
        'dish_name': dish[2],
    })

    # Удаление предыдущего сообщения
    await call.message.delete()

    message_obj = await bot.send_message(
        chat_id=user,
        text=f"💫 Блюдо:\n"
             f"<i>«{dish[2]}»</i>\n"
             f"\n"
             f"Если хотите оставить письменный отзыв, напиши его в ответ на это сообщение 🙏🏻\n"
             f"\n"
             f"Спасибо!",
        reply_markup=buttons_05()
    )
    db.set_temp_users_state(user, 'review_end')
    db.set_temp_users_message_id(user, message_obj.message_id)
    db.add_user_action(user, 'Пользователь оставил отзыв')


def buttons_05():
    menu = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(text="Пропустить ❌",
                                callback_data=f"review_end")

    menu.row(btn1)

    return menu


def buttons_food_05(dish_id: int, dish: int, length: int, last: int, in_basket: bool = None, qr_scanned: bool = None, quantity: int = 0, size_list: list = None, user: int = 0):
    menu = InlineKeyboardMarkup(row_width=3)
    if dish is not None:
        if length != 1:
            if dish > 0:
                btn1 = InlineKeyboardButton(text=f"⏪",
                                            callback_data="send_dish_back")

                if last == 0:
                    menu.row(btn1)
                else:
                    btn2 = InlineKeyboardButton(text=f"⏩",
                                                callback_data="send_dish_next")
                    menu.row(btn1, btn2)
            else:
                btn2 = InlineKeyboardButton(text=f"⏩",
                                            callback_data="send_dish_next")
                menu.add(btn2)
        if qr_scanned:
            if in_basket:
                if quantity > 1:
                    btn0 = InlineKeyboardButton(text=f"Убрать из 🛒 ({quantity})",
                                                callback_data=f"basket_remove")
                else:
                    btn0 = InlineKeyboardButton(text="Убрать из 🛒",
                                                callback_data=f"basket_remove")
                if size_list:
                    btn_extra = InlineKeyboardButton(text="+ 1",
                                                     callback_data=f"choice_size_{dish_id}")
                else:
                    btn_extra = InlineKeyboardButton(text="+ 1",
                                                callback_data=f"basket_add")
                menu.add(btn0)
                menu.add(btn_extra)
            else:
                if size_list:
                    btn0 = InlineKeyboardButton(text="Добавить в 🛒",
                                                callback_data=f"choice_size_{dish_id}")
                else:
                    btn0 = InlineKeyboardButton(text="Добавить в 🛒",
                                                callback_data=f"basket_add")
                menu.add(btn0)
            btn3 = InlineKeyboardButton(text="Перейти к ➡️ 🛒", callback_data="check_order")
            menu.add(btn3)
    # menu_start
    btn1 = InlineKeyboardButton(text="⬅️ Вернуться к категориям",
                                callback_data="watch_menu_again")

    menu.add(btn1)
    return menu


@dp.message_handler(commands=['boss'])
async def boss_shemodi(message: types.Message):
    user = message.from_user.id
    await bot.delete_message(user, message.message_id)
    message_obj = await bot.send_message(
        chat_id=user,
        text="Введите пароль: ",
    )
    db.set_temp_users_state(user, 'boss')
    db.set_temp_users_message_id(user, message_obj.message_id)


@dp.callback_query_handler(text_contains="review_end")
async def review_end(call: types.CallbackQuery):
    await call.answer()
    user_first_name = db.get_users_user_first_name(call.from_user.id)
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text=f"<b>{user_first_name}</b>, оставь отзыв о выбранных блюдах в ресторане <b>Korean Chick</b> \n\n"
                                     f"Нейросеть food2mood учтёт твои комментарии при формировании персональных рекомендаций в будущем 😏🔜",
                                reply_markup=buttons_02()
    )


def buttons_02():
    menu = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton(text="⏮️ Вернуться на главную",
                                callback_data="menu_start")

    btn2 = InlineKeyboardButton(text="Оставить ещё один отзыв 🆕", callback_data="leave_a_review")

    btn3 = InlineKeyboardButton(text="Мои f2m коины 🪙", callback_data="food_to_mood_coin_status")

    menu.add(btn1)
    menu.add(btn2)

    return menu


@dp.callback_query_handler(text_contains='menu_start')
async def return_to_start(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id
    text = (f"<b>Привет, дорогой друг!\n"
            "Как ты хочешь сделать заказ? </b>☺️🙏")
    await call.message.delete()
    message_obj = await bot.send_message(
        chat_id=user,
        text=text,
        parse_mode='HTML',
        reply_markup=buttons_start_02()
    )