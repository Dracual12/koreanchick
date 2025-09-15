from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.deep_linking import decode_payload
from config import dp, bot, db
from datetime import datetime
from waiters import waiter_start as w_start
import time
import sys
import os

# Добавляем путь к корневой папке для импорта webapp_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from webapp_config import get_webapp_url

async def start_handler(message: types.Message):
    user = message.from_user.id
    user_id = str(user)
    reg_time = datetime.utcnow().replace(microsecond=0)
    
    # Логируем ФИО пользователя в сессию
    fio = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    if fio:
        db.update_logging_session_fio(user_id, fio)
    
    # Логируем телефон пользователя в сессию (если есть)
    phone = db.get_users_phone(user)
    if phone:
        db.update_logging_session_phone(user_id, phone)
    
    # Новый пользователь:
    if db.check_basket_exists(user):
        db.set_basket(user, "{}")
    else:
        db.create_basket(user)
    if not db.check_users_user_exists(user):
        db.add_users_user(
            user,
            f'tg://user?id={user}',
            reg_time,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        db.set_default_q1(user)
        db.set_default_q2(user)
        text = f'\n🙋🏻‍♂️Новый посетитель:' \
               f'\n' \
               f'\n<b>{message.from_user.first_name} {message.from_user.last_name}</b>' \
               f'\n@{message.from_user.username}' \
               f'\nid <a href="tg://user?id={user}">{user}</a>' \
               f'\n' \
               f'\n<code>{reg_time}</code>'

        # await bot.send_message(admin, text)
        db.set_users_mode(user, 0, 'start')

    # Получаем ID предыдущих сообщений
    first = int(db.get_users_first_message(user))
    last = int(db.get_users_last_message(user))

    # Очистка чата:
    if first != 0 and last != 0:
        for i in range(first, last + 1):
            try:
                await bot.delete_message(user, i)
            except Exception as ex:
                pass

    # Сбрасываем счетчики сообщений
    db.set_users_first_message(user, 0)
    db.set_users_last_message(user, 0)

    # Действие:
    db.set_users_mode(user, 0, 'start')
    text = (f"<b>Привет, дорогой друг!\n"
            "Как ты хочешь сделать заказ? </b>☺️🙏")

    message_obj = await bot.send_message(
        chat_id=user,
        text=text,
        parse_mode='HTML',
        reply_markup=buttons_start_02()
    )
    # Сохраняем ID нового сообщения
    if db.get_users_temp_message_id(user) is None:
        db.set_first_temp_mes_id(user, message_obj.message_id)
    else:
        db.set_temp_users_message_id(user, message_obj.message_id)
    db.set_users_first_message(user, message_obj.message_id)
    db.set_users_last_message(user, message_obj.message_id)


@dp.message_handler(commands=['start', 'restart'])
async def start_command(message: types.Message):
    user = message.from_user.id
    # Начинаем новую сессию логирования
    db.start_logging_session(str(user))
    # Проверяем наличие аргументов
    args = message.get_args()
    if not args:
        # Если аргументов нет, просто показываем стартовое меню
        db.set_qr_scanned(user, False)
        await start_handler(message)
        return

    try:
        decoded_args = decode_payload(args)
    except Exception as e:
        print(f"Error decoding args: {e}")
        await start_handler(message)
        return

    if "or" in decoded_args[:2]:
        if db.check_waiter_exists(user):
            db.clear_remark(user)
            await w_start.get_order(message, decoded_args[2:])
        else:
            await bot.send_message(chat_id=user, text="Вы не зарегистрированы как официант")
    elif db.check_users_user_exists(message.from_user.id):
        # Пользователь уже существует, показываем стартовое меню
        await start_handler(message)
    else:
        # Новый пользователь, показываем стартовое меню
        await start_handler(message)


@dp.message_handler(commands=['webapp'])
async def webapp_command(message: types.Message):
    """Команда для открытия Web App"""
    user = message.from_user.id
    
    webapp_url = get_webapp_url()
    
    text = ("<b>�� Откройте наше веб-приложение!</b>\n\n"
            "В веб-приложении вы можете:\n"
            "• 📱 Просматривать меню в удобном интерфейсе\n"
            "• 🛒 Добавлять блюда в корзину\n"
            "• 📋 Оформлять заказы с QR-кодом\n"
            "• 📊 Просматривать историю заказов\n"
            "• ⭐ Получать персональные рекомендации\n\n"
            "Нажмите кнопку ниже, чтобы открыть приложение:")
    
    keyboard = InlineKeyboardMarkup()
    webapp_button = InlineKeyboardButton(
        text="🌐 Открыть Web App",
        web_app=WebAppInfo(url=webapp_url)
    )
    keyboard.add(webapp_button)
    
    await bot.send_message(
        chat_id=user,
        text=text,
        parse_mode='HTML',
        reply_markup=keyboard
    )


def buttons_start_02():
    menu = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(text="В зале 🏠",
                                callback_data="order_at_rest")

    btn2 = InlineKeyboardButton(text="Доставка 🚘",
                                callback_data="order_at_delivery")

    # Добавляем кнопку Web App
    btn3 = InlineKeyboardButton(
        text="🌐 Веб-приложение",
        web_app=WebAppInfo(url=get_webapp_url())
    )

    menu.add(btn1)
    menu.add(btn2)
    menu.add(btn3)

    return menu
