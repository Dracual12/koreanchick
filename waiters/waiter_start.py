import logging
import random
import datetime

import requests
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
import time
import handlers.auxiliary_functions as af
import iiko_f.iiko as iiko_f
from iiko_f.iiko import name_and_terminal_id
from naim.main import dp, bot, db
#from handlers import menu_food

icons = {
    'Меню от шефа': '👨‍🍳',
    'Чебуреки': '🥟',
    'Хинкали': '🇬🇪',
    'Выпечка': '🥧',
    'Сезонное меню': '📋',
    'Мангал': '🫓',
    'Горячее Рыба': '🐟',
    'Детское меню': '🧒',
    "Салаты и закуски": "🥗",
    "Первые блюда": "🍲",
    "Горячие блюда": "🍛",
    "Гарниры": "🍚",
    "Десерты": "🍰",
    "Напитки": "☕",
    "Завтрак": "🍳",
    "Ужин": "🍽️",
    "Японская кухня": "🍣",
    "Поке": "🥢",
    "Холодные закуски": "❄️",
    "Закуски": "😋",
    "Салаты": "🥗",
    "Супы": "🍲",
    "Паста": "🍝",
    "Горячие закуски": "🔥",
    "Хлеб": "🍞",
    "Соус": "🧉",
    "Дары моря": "🦞",
    "Мясо и птица": "🥩",
    "Радость": "🤩",
    "Печаль": "😢",
    "Гнев": "😡",
    "Спокойствие": "😌",
    "Волнение": "😬",
    "Нутрициолог": "👩🏻‍💻",
    "Пользователи": "🙋🏻‍♀️",
    "Обломов": "⭐",
    "Ивлев": "⭐",
    'Грузинская':'🇬🇪',
    'Европейская':'🇪🇺',
    'Французская':'🇫🇷',
    1: "🥇",
    2: "🥈",
    3: "🥉",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
    11: "1️⃣1️⃣",
    12: "1️⃣2️⃣",
    13: "1️⃣3️⃣",
    14: "1️⃣4️⃣",
    15: "1️⃣5️⃣",
    16: "1️⃣6️⃣",
    17: "1️⃣7️⃣",
    18: "1️⃣8️⃣",
    19: "1️⃣9️⃣",
    20: "2️⃣0️⃣",
    21: "2️⃣1️⃣",
    22: "2️⃣2️⃣",
    23: "2️⃣3️⃣",
    24: "2️⃣4️⃣",
    25: "2️⃣5️⃣",
    26: "2️⃣6️⃣",
    27: "2️⃣7️⃣",
    28: "2️⃣8️⃣",
    29: "2️⃣9️⃣",
    30: "3️⃣0️⃣",
    31: "3️⃣1️⃣",
    32: "3️⃣2️⃣",
    33: "3️⃣3️⃣",
    34: "3️⃣4️⃣",
    35: "3️⃣5️⃣",
    36: "3️⃣6️⃣",
    37: "3️⃣7️⃣",
    38: "3️⃣8️⃣",
    39: "3️⃣9️⃣",
    40: "4️⃣0️⃣",
    41: "4️⃣1️⃣",
    42: "4️⃣2️⃣",
    43: "4️⃣3️⃣",
    44: "4️⃣4️⃣",
    45: "4️⃣5️⃣",
    46: "4️⃣6️⃣",
    47: "4️⃣7️⃣",
    48: "4️⃣8️⃣",
    49: "4️⃣9️⃣",
    50: "5️⃣0️⃣",
    'Галочка': "✅"
}

def waiter_action(first_name, location):
    print(f"│ [{time.time()}] {first_name} → {location}")

def calculating_the_order_amount(user):
    amount = sum([db.get_dish_price_by_name(e) for e in list(eval(db.get_basket(user)).keys())])
    return amount

async def check_order_in_table(table):
    pass


async def start(message: types.Message):
    name = message.text.split()
    waiter = message.from_user.id
    data = message.text.split(':')
    id = db.get_users_temp_message_id(waiter)[0]
    try:
        # Новый официант:
        if not db.check_waiter_exists(waiter):
            # Регистрируем официанта:
            db.add_waiter(
                waiter,
                f'tg://user?id={waiter}',
                message.from_user.username,
                name[0],
                name[1],
                name[2]
            )
            text = (
                f'\n🙋🏻‍♂️Новый официант:'
                f'\n<b>{name[0]} {name[1]} {name[2]}</b>'
                f'\n@{message.from_user.username}'
                f'\nid <a href="tg://user?id={waiter}">{waiter}</a>\n'
            )
            await bot.delete_message(waiter, message.message_id)
            await bot.delete_message(waiter, id)
            await bot.send_message(waiter, text)
        else:
            text = '\nТы уже зарегистрировался(ась) как официант'
            await bot.edit_message_text(waiter, id, text)
    except Exception as e:
        text = '\nОшибка ввода ФИО'
        print(e)
        await bot.delete_message(waiter, id)
        await bot.send_message(waiter, text)


async def get_order(message: types.Message, client_id):
    waiter = message.from_user.id
    # Проверяем официанта:
    if db.check_waiter_exists(waiter):
        try:
            await set_order(waiter, client_id)
        except Exception as e:
            print(e)


def order_status(waiter):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="+", switch_inline_query_current_chat='')
    btn2 = InlineKeyboardButton(text="-", callback_data="d_from_order")
    btn3 = InlineKeyboardButton(text="Принять заказ", callback_data="order_accepted")
    btn4 = InlineKeyboardButton(text="Ред. заметку",callback_data="edit_remark")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup


@dp.callback_query_handler(text_contains="edit_remark")
async def edit_remark(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id
    if '2' in call.data:
        remark = db.get_remark(user).split('\n')
        remark.remove(call.data.split('_')[-1])
        if len(remark) > 0:
            db.set_remark(user, '\n'.join(remark))
        else:
            db.set_remark(user, '')
    remark = db.get_remark(user)
    if len(remark) > 0:
        keyboard = InlineKeyboardMarkup()
        for e in remark.split('\n'):
            btn = InlineKeyboardButton(text=f'{e}', callback_data=f'edit_remark_2_{e}')
            keyboard.add(btn)

        keyboard.add(InlineKeyboardButton(text=f'⬅️ Назад', callback_data=f'back_to_order'))
        await bot.edit_message_text(chat_id=user, message_id=call.message.message_id,
                                    text='Какой пункт заметки Вы хотите удалить', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=f'⬅️ Назад', callback_data=f'back_to_order'))
        await bot.edit_message_text(chat_id=user, message_id=call.message.message_id,
                                    text='Заметок нет', reply_markup=keyboard)


async def dish_added(waiter, dish_id):
    client_id = eval(db.get_waiter_score(waiter))[-1]
    dish = db.restaurants_get_by_id(dish_id)[2]
    try:
        basket = eval(db.get_basket(client_id))
    except Exception as e:
        print("waiter error", e)
        basket = {}
    if dish not in basket:
        basket[dish] = [dish_id, 1, [None]]
    else:
        basket[dish][1] += 1
        basket[dish][2].append(None)
    db.set_basket(client_id, str(basket))
    await set_order(waiter, client_id, message_id=db.get_users_temp_message_id(waiter)[0])


@dp.callback_query_handler(text_contains="d_from_order")
async def d_from_order(call: types.CallbackQuery):
    await call.answer()
    waiter = call.from_user.id
    client_id = eval(db.get_waiter_score(waiter))[-1]
    data = call.data.split('_')
    try:
        basket = eval(db.get_basket(client_id))
    except Exception as e:
        print("waiter error", e)
        basket = {}
    if len(data) > 3:
        dish_id = data[-1]
        dish = db.restaurants_get_by_id(dish_id)[2]
        if basket[dish][1] > 1:
            basket[dish][1] -= 1
            basket[dish][2].pop()
        else:
            try:
                basket.pop(dish, None)
            except ValueError:
                pass
        db.set_basket(client_id, str(basket))
    await bot.edit_message_text(
        chat_id=waiter,
        message_id=call.message.message_id,
        text="Нажмите на позицию чтобы удалить",
        reply_markup=change_order(basket)
    )


def change_order(basket):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for dish in basket:
        if basket[dish][1] > 1:
            btn = InlineKeyboardButton(text=f"{dish} ({basket[dish][1]})",
                                       callback_data=f"d_from_order_{basket[dish][0]}")
        else:
            btn = InlineKeyboardButton(text=f"{dish}",
                                       callback_data=f"d_from_order_{basket[dish][0]}")
        keyboard.row(btn)
    btn1 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_order")
    keyboard.row(btn1)
    return keyboard


@dp.callback_query_handler(text_contains="back_to_order")
async def back_to_order(call: types.CallbackQuery):
    await call.answer()
    waiter = call.from_user.id
    client_id = eval(db.get_waiter_score(waiter))[-1]
    await set_order(waiter, client_id, message_id=call.message.message_id)


@dp.callback_query_handler(text_contains="order_accepted")
async def order_table(call: types.CallbackQuery):
    waiter = call.from_user.id
    await call.answer()
    message_obj = await bot.edit_message_text(
        chat_id=waiter,
        message_id=call.message.message_id,
        text="Введите номер столика"
    )
    db.set_temp_users_message_id(waiter, message_obj.message_id)
    db.set_temp_users_state(waiter, 'order_table')


async def order_accepted(waiter, client_id, table_number):
    db.add_order(waiter, table_number, datetime.datetime.now(), calculating_the_order_amount(client_id))
    if db.get_current_earnings(waiter):
        cur_waiter_earnings = db.get_current_earnings(waiter) + calculating_the_order_amount(client_id)
    else:
        db.set_current_earnings(calculating_the_order_amount(client_id), waiter)
    if not db.get_waiter_score(waiter):
        temp_list = [client_id]
    else:
        temp_list = eval(db.get_waiter_score(waiter))
        temp_list.append(client_id)
    db.set_waiter_score(waiter, str(temp_list))
    try:
        basket = eval(db.get_basket(client_id))
    except Exception as e:
        print("waiter error", e)
        basket = {}
    order_text = ""
        #check_order_in_table()
    items = [{'productId': db.get_iiko_id_by_name(e) if basket[e][2][0] is None else iiko_f.korean_chick_iiko_id[e + ' ' + basket[e][2][0]], 'price': db.get_dish_price_by_name(e), 'type': 'Product', 'amount': basket[e][1]} for e in basket]
    #iiko_f.add_order(db.check_token(rest.split(':')[0], iiko_f.API_KEYS[rest.split(':')[0]]), iiko_f.name_and_iiko_id[iiko_f.name_and_iiko_name[rest.split(':')[0]]], iiko_f.name_and_terminal_id[iiko_f.name_and_iiko_name[rest.split(':')[0]]], items)

    i = 0
    for dish in basket:
        i += 1
        if basket[dish][1] > 1:
            order_text += f"{af.ind_to_number(i)} {dish} ({basket[dish][1]})\n"
        else:
            order_text += f"{af.ind_to_number(i)} {dish}\n"
    text = (
        f'\n<b>Заказ принят!</b>\n'
        f"<b>Настроение гостя:</b> {db.get_temp_users_mood(client_id)}{icons[db.get_temp_users_mood(client_id)]}\n\n"
        f'{order_text}\n'
    )
    remark = get_remark(waiter, client_id)
    if remark:
        text += f"\n<b>Заметка:</b>\n\n{remark}\n"
    text += f'\n<b>Количество твоих уникальных заказов: {len(set(temp_list))}</b>'

    db.set_temp_users_state(waiter, 'get_order')
    await bot.edit_message_text(chat_id=waiter, message_id=db.get_users_temp_message_id(waiter)[0], text=text)
    await bot.delete_message(chat_id=waiter, message_id=db.get_users_temp_message_id(waiter))
    #await menu_food.bon_appetite_2(client_id)


async def set_order(waiter, client_id, message_id=None):
    if not db.get_waiter_score(waiter):
        temp_list = [client_id]
    else:
        temp_list = eval(db.get_waiter_score(waiter))
        temp_list.append(client_id)
    db.set_waiter_score(waiter, str(temp_list))
    try:
        basket = eval(db.get_basket(client_id))
    except Exception as e:
        print("waiter error", e)
        basket = {}
    order_text = ""
    additional_dishes = []
    basket2 = list(eval(db.get_basket(client_id)).keys())
    for i in range(len(basket2)):
        if db.additional_dishes(basket2[i]):
            additional_dishes.append(f'{af.ind_to_number(i + 1)} {db.additional_dishes(basket2[i])}')

    i = 0
    for dish in basket:
        i += 1
        if basket[dish][1] > 1:
            order_text += f"{af.ind_to_number(i)} {dish} ({basket[dish][1]}) "
        else:
            order_text += f"{af.ind_to_number(i)} {dish} "
        if basket[dish][2][0] != None:
            order_text += basket[dish][2][0]
        order_text += '\n'
    text = (
        f'\n<b>Новый заказ {len(set(temp_list)) + 1}:</b>\n'
        f"<b>Настроение гостя:</b> {db.get_temp_users_mood(client_id)} {icons[db.get_temp_users_mood(client_id)]}\n\n"
        f'——————————————\n'
        f'{order_text}'
        f'——————————————\n\n'
    )
    remark = get_remark(waiter, client_id)
    if remark:
        text += f"<b>Заметка:</b>\n\n{remark}\n"
        text += f'——————————————\n'
    if remark:
        message_id = db.get_users_temp_message_id(waiter)[0]
    if len(additional_dishes) > 0:
        text += '<i>Подсказка по доп.продаже:</i>\n'
        for e in additional_dishes:
            text+= f"<i>{e}</i>\n"
    text += f'\n<blockquote>Отправь сообщение с текстом боту, чтобы добавить <b>Заметку</b> к заказу</blockquote>'
    if message_id:
        message_obj = await bot.edit_message_text(
            chat_id=waiter,
            message_id=message_id,
            text=text,
            reply_markup=order_status(waiter)
        )
    else:
        message_obj = await bot.send_message(
            chat_id=waiter,
            text=text,
            reply_markup=order_status(waiter)
        )
    db.set_temp_users_message_id(waiter, message_obj.message_id)
    db.set_temp_users_state(waiter, 'get_order')

remarks_storage = {}
async def save_remark(waiter, client_id, remark):
    existing = db.get_remark(waiter)
    if existing:
        new_remark = existing + "\n" + remark
    else:
        new_remark = remark
    db.set_remark(waiter, new_remark)

def get_remark(waiter, client_id):
    return db.get_remark(waiter)


@dp.callback_query_handler(text_contains="make_remark")
async def process_make_remark(call: types.CallbackQuery):
    await call.answer()
    waiter = call.from_user.id
    message_obj = await bot.edit_message_text(
        chat_id=waiter,
        message_id=call.message.message_id,
        text="Введите вашу заметку:"
    )
    db.set_temp_users_message_id(waiter, message_obj.message_id)
    db.set_temp_users_state(waiter, 'waiter_make_remark')