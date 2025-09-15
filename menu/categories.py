import ast
import os
import time

from config import db, dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import types

from iiko_f.iiko import korean_chick_portion_price
from menu import sort_the
import handlers.auxiliary_functions as af
from files.icons import icons

# ======================================================================================================================
# ===== Обработка callbacks =================================================================================================
# ======================================================================================================================


@dp.callback_query_handler(text_contains='watch_menu')
async def watch_menu(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id
    text = 'Выбери категорию меню 🔍'
    if 'again' in call.data:
        await bot.delete_message(chat_id=user, message_id=call.message.message_id)
        await bot.send_message(chat_id=user, text=text, reply_markup=create_menu_buttons())
    else:

        await bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=text,
                                reply_markup=create_menu_buttons())


@dp.callback_query_handler(text_contains='category_menu')
async def category_menu(call: types.CallbackQuery):
    await call.answer()
    category = call.data.split('_')[-1]
    user = call.from_user.id
    await bot.delete_message(chat_id=user, message_id=call.message.message_id)
    # Если предполагается, что название категории может содержать подчеркивания
    if category:  # Проверка на наличие категории
        db.set_temp_users_category(user, category)
    db.set_client_temp_dish(user, 0)
    dish, length, numb = sort_the.get_dish(user)
    try:
        dish_id = db.restaurants_get_dish(dish['Название'])[0]
    except Exception as e:
        dish_id = None

    if dish is not None:
        text = af.generate_dish_text(user, icons, dish, length, numb, dish_id)
        await bot.send_message(chat_id=user, text=text, reply_markup=buttons_food_05(dish_id, dish, length, numb, False, db.get_qr_scanned(user), 0, None, user))
    else:
        await bot.send_message(chat_id=user, text="Блюда не найдены", reply_markup=create_back_to_cat_buttons())


@dp.callback_query_handler(text_contains='send_dish')
async def send_dish(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id
    dish, length, numb = sort_the.get_dish(user)
    try:
        dish_id = db.restaurants_get_dish(dish['Название'])[0]
    except Exception as e:
        dish_id = None

    if dish is not None:
        text = af.generate_dish_text(user, icons, dish, length, numb, dish_id)
        await bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=text,
                                reply_markup=buttons_food_05(dish_id, dish, length, numb, False, db.get_qr_scanned(user), 0, None, user))
    else:
        await bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text="Блюда не найдены",
                                reply_markup=create_back_to_cat_buttons())


@dp.callback_query_handler(text_contains='return_to_recommendation')
async def return_to_recommendation(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id
    dish, length, numb = sort_the.get_dish(user)
    try:
        dish_id = db.restaurants_get_dish(dish['Название'])[0]
    except Exception as e:
        dish_id = None

    if dish is not None:
        text = af.generate_dish_text(user, icons, dish, length, numb, dish_id)
        await bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=text,
                                reply_markup=buttons_food_05(dish_id, dish, length, numb, False, db.get_qr_scanned(user), 0, None, user))
    else:
        await bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text="Блюда не найдены",
                                reply_markup=create_back_to_cat_buttons())


def create_back_to_cat_buttons():
    menu = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton(text="⬅️ Назад",
                                    callback_data='watch_menu')
    menu.add(back_btn)
    return menu


def create_menu_buttons():
    menu = InlineKeyboardMarkup()
    for e in db.get_all_categories():
        menu.add(InlineKeyboardButton(text=f"{e} {icons[e]}",
                                      callback_data=f"category_menu_{e}"))
    back_btn = InlineKeyboardButton(text="⬅️ Назад",
                                    callback_data="confirmation_of_the_second_q")
    menu.add(back_btn)
    return menu


def create_buttons_to_menu(user):
    menu = InlineKeyboardMarkup()
    if db.get_qr_scanned(user):
        btn3 = InlineKeyboardButton(text="Добавить в 🛒", callback_data="rec_to_b")
        menu.add(btn3)
    
    btn1 = InlineKeyboardButton(text=f"Ознакомиться с меню 🧾",
                                callback_data=f"watch_menu")

    # Добавляем кнопку Web App
    btn_webapp = InlineKeyboardButton(
        text="🌐 Открыть веб-приложение",
        web_app=WebAppInfo(url="https://your-domain.com")  # Замените на реальный URL
    )

    btn2 = InlineKeyboardButton(text="⬅️ Назад",
                                callback_data="confirmation_of_the_first_q")
    menu.add(btn1)
    menu.add(btn_webapp)  # Добавляем кнопку Web App
    menu.add(btn2)
    return menu


def buttons_food_05(dish_id: int, dish: int, length: int, last: int, in_basket: bool = None, qr_scanned: bool = None, quantity: int = 0, size_list: list = None, user: int = 0):
    menu = InlineKeyboardMarkup(row_width=2)
    
    # Основные кнопки
    if not in_basket:
        btn1 = InlineKeyboardButton(text="Добавить в 🛒", callback_data=f"basket_{dish_id}")
    else:
        btn1 = InlineKeyboardButton(text=f"В корзине ({quantity})", callback_data=f"basket_{dish_id}")
    
    btn2 = InlineKeyboardButton(text="⬅️ Назад", callback_data="send_dish")
    btn3 = InlineKeyboardButton(text="➡️ Далее", callback_data="send_dish")
    
    # Кнопка Web App
    btn_webapp = InlineKeyboardButton(
        text="🌐 Веб-приложение",
        web_app=WebAppInfo(url="https://your-domain.com")  # Замените на реальный URL
    )
    
    menu.add(btn1)
    menu.add(btn2, btn3)
    menu.add(btn_webapp)  # Добавляем кнопку Web App
    
    return menu


# Остальной код остается без изменений...
# (Здесь должен быть весь остальной код из оригинального файла)
