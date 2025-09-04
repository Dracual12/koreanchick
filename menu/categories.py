import ast
import os
import time

from config import db, dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
        size_list = dish['Размер']
        if size_list:
            size_list = eval(size_list)
        photo_dir = '/Users/artemijpetrov/PycharmProjects/koreanchickdouble/chick'

        all_files = {os.path.splitext(file)[0]: os.path.join(photo_dir, file) for file in os.listdir(photo_dir)}
        shemodi_dish_photo = False
        photo_shemodi = ''
        for j in all_files:
            if j in dish['Название'] or dish['Название'] in j:
                shemodi_dish_photo = True
                photo_shemodi = j
        if shemodi_dish_photo or (dish['Название'] in all_files and dish['Ресторан'] == 'Молодёжь'):
            if shemodi_dish_photo:
                file_path = all_files[photo_shemodi]
            else:
                file_path = all_files[dish['Название']]
            if os.path.isfile(file_path):

                message_obj = await bot.send_photo(user, open(file_path, 'rb'),
                                                   caption=text,
                                                   reply_markup=buttons_food_05(dish_id,
                                                                                db.get_client_temp_dish(user),
                                                                                length, numb, in_basket,
                                                                                bool(db.get_qr_scanned(user)), quantity,
                                                                                size_list, user))
            else:
                message_obj = await bot.edit_message_text(
                    chat_id=user,
                    message_id=call.message.message_id,
                    text=text,

                    reply_markup=buttons_food_05(dish_id, db.get_client_temp_dish(user), length, numb, in_basket,
                                                 bool(db.get_qr_scanned(user)), quantity, size_list, user)
                )
        else:
            message_obj = await bot.edit_message_text(
                chat_id=user,
                message_id=call.message.message_id,
                text=text,
                reply_markup=buttons_food_05(dish_id, db.get_client_temp_dish(user), length, numb, in_basket,
                                             bool(db.get_qr_scanned(user)), quantity, size_list, user)
            )
        db.set_temp_users_dish_id(user, db.restaurants_get_dish(dish['Название'])[0])

    else:
        message_obj = await bot.send_message(
            chat_id=user,
            text=f"🍤"
                 f"<b>Кажется, в этом заведении нет блюд, подходящих под ваши критерии</b> 🤔\n"
                 f"\n"
                 f"Попробуй поменять категорию блюд, настроение или список продуктов, которые ты не употребляешь в пищу 😉\n",
            reply_markup=create_back_to_cat_buttons()
        )
    db.set_temp_users_message_id(user, message_obj.message_id)


# ======================================================================================================================
# ===== Создание клавиатур =================================================================================================
# ======================================================================================================================

def create_back_to_cat_buttons():
    menu = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton(text="⬅️ Назад", callback_data='watch_menu')
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

    btn2 = InlineKeyboardButton(text="⬅️ Назад",
                                callback_data="confirmation_of_the_first_q")
    menu.add(btn1)
    menu.add(btn2)
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


@dp.callback_query_handler(text_contains=f"choice_size")
async def choice_size(call: types.CallbackQuery):
    await call.answer()
    try:
        user = call.from_user.id
        text = "<b>Выбери размер порции:</b>"
        dish_id = int(call.data.split("_")[-1])


        # Получаем информацию о блюде
        dish_data = db.restaurants_get_by_id(dish_id)
        if not dish_data or len(dish_data) < 5:
            await bot.answer_callback_query(call.id, "Ошибка: информация о блюде не найдена", show_alert=True)
            return

        dish_name = dish_data[2]

        # Получаем список доступных размеров
        size_list = db.get_dish_size(dish_id)
        if not size_list:
            await bot.answer_callback_query(call.id, "Ошибка: размеры порций не найдены", show_alert=True)
            return

        # Создаем клавиатуру с размерами
        keyboard = size_keyboard(size_list, dish_name)
        # Отправляем сообщение с выбором размера
        await bot.delete_message(
            chat_id=user,
            message_id=call.message.message_id)
        await bot.send_message(chat_id=user,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    except Exception as e:
        # logger.error(f"Error in choice_size: {str(e)}")
        print(e)
        await bot.answer_callback_query(call.id, "Произошла ошибка при выборе размера", show_alert=True)


def size_keyboard(size_list, dish_name=None):
    keyboard = InlineKeyboardMarkup(row_width=1)
    size_list = ast.literal_eval(size_list)
    for size in size_list:
        if dish_name and size.startswith(dish_name):
            # Для Korean Chick показываем только размер и цену
            display_text = size.replace(dish_name, '').strip() + f" ({korean_chick_portion_price[size]} руб.)"
            btn = InlineKeyboardButton(text=display_text,
                                       callback_data=f"basket_add_{size}")
        else:
            btn = InlineKeyboardButton(text=f"{size}",
                                       callback_data=f"basket_add_{size}")
        keyboard.row(btn)
    return keyboard



@dp.callback_query_handler(text_contains='rec_to_b')
async def add_recommendation_to_basket(call: types.CallbackQuery):
    user = call.from_user.id
    await call.answer()
    recommendation = eval(db.get_temp_rec(user))

    if not recommendation:
        await bot.answer_callback_query(call.id, "Нет доступных рекомендаций", show_alert=True)
        return

    if not db.check_basket_exists(user):
        db.create_basket(user)

    basket = eval(db.get_basket(user))
    added_dishes = 0

    for dish in recommendation:
        dish_name = dish[1]
        try:
            dish_info = get_dish_info(dish_name)
            if not dish_info:
                continue

            dish_id, dish_data, size_list = dish_info

            # Для Korean Chick проверяем наличие размеров

            if dish_name not in basket:
                basket[dish_name] = [dish_id, 1, [None]]
            else:
                basket[dish_name][1] += 1
                basket[dish_name][2].append(None)

            added_dishes += 1
        except Exception as e:
            print(f"Error adding dish {dish_name} to basket: {e}")
            continue

    db.set_basket(user, str(basket))

    if added_dishes > 0:
        # Обновляем текущее сообщение с рекомендациями
        recommendation_text = f"<b>🔝 В ресторане «KoreanChick» нейросеть food2mood рекомендует тебе:</b>\n\n"
        for dish in recommendation:
            recommendation_text += f"{dish[0]} <i>{dish[1]}</i>\n"
        recommendation_text += (
            "\n<blockquote>Нажми <b>Ознакомиться с мeню</b> 🧾, чтобы поменять рекимендации и детальнее изучить блюда! 👀</blockquote>")
        # Создаем новую клавиатуру с кнопками
        keyboard = InlineKeyboardMarkup(row_width=1)

        # Добавляем кнопки для управления корзиной
        keyboard.add(
            InlineKeyboardButton(text="Убрать из 🛒", callback_data="remove_recommendation"),
            InlineKeyboardButton(text="+1", callback_data="add_more_recommendation")
        )

        # Добавляем кнопку "Сделать заказ"
        keyboard.add(InlineKeyboardButton(text="Перейти к ➡️ 🛒️", callback_data="check_order2"))

        # Добавляем остальные кнопки
        keyboard.add(
            InlineKeyboardButton(text="Ознакомиться с меню 🧾", callback_data="watch_menu"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_rest_search")
        )

        await bot.edit_message_text(
            chat_id=user,
            message_id=call.message.message_id,
            text=recommendation_text,
            reply_markup=keyboard
        )
    else:
        await bot.answer_callback_query(call.id, "Не удалось добавить блюда в корзину", show_alert=True)


def get_dish_info(dish_name: str):

    try:
        # Получаем ID блюда
        dish_id_data = db.restaurants_get_dish(dish_name)
        if not dish_id_data:
            return None

        dish_id = dish_id_data[0]

        # Получаем полную информацию о блюде
        dish_data = db.restaurants_get_by_id(dish_id)
        if not dish_data or len(dish_data) < 5:
            return None

        # Проверяем наличие размеров порций
        size_list = None
        if len(dish_data) > 21 and dish_data[21]:
            try:
                size_list = eval(dish_data[21])
            except:
                size_list = None

        return dish_id, dish_data, size_list
    except Exception as e:
        print(f"Error in get_dish_info: {e}")
        return None


@dp.callback_query_handler(text_contains='remove_recommendation')
async def remove_recommendation_from_basket(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id

    recommendation = eval(db.get_temp_rec(user))

    if not recommendation:
        await bot.answer_callback_query(call.id, "Нет доступных рекомендаций", show_alert=True)
        return

    basket = eval(db.get_basket(user))
    removed_dishes = 0

    # Удаляем все блюда из рекомендаций
    for dish in recommendation:
        dish_name = dish[1]
        if dish_name in basket:
            if basket[dish_name][1] > 1:
                basket[dish_name][1] -= 1
                basket[dish_name][2].pop()
            else:
                del basket[dish_name]
            removed_dishes += 1

    if removed_dishes > 0:
        db.set_basket(user, str(basket))

        # Если корзина пуста, обновляем сообщение
        if not basket:
            recommendation_text = f"<b>🔝 В ресторане «KoreanChick» нейросеть food2mood рекомендует тебе:</b>\n\n"
            for dish in recommendation:
                recommendation_text += f"{dish[0]} <i>{dish[1]}</i>\n"
                recommendation_text += (
                "\n<blockquote>Нажми <b>Ознакомиться с мeню</b> 🧾, чтобы поменять рекимендации и детальнее изучить блюда! 👀</blockquote>")
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton(text="Добавить в 🛒", callback_data="rec_to_b"))
            keyboard.add(InlineKeyboardButton(text="Ознакомиться с меню 🔀", callback_data="show_categories"))
            keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_rest_search"))

            await bot.edit_message_text(
                chat_id=user,
                message_id=call.message.message_id,
                text=recommendation_text,
                reply_markup=keyboard
            )
    else:
        await bot.answer_callback_query(call.id, "Нет блюд для удаления", show_alert=True)
