from config import dp, bot, db
from aiogram import types
import questiionnaire
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from handlers.message_handlers import create_web_app_button


@dp.callback_query_handler(text_contains=f"order_at")
async def order_at(call: types.CallbackQuery):
    await call.answer()
    user = call.from_user.id
    if 'rest' in call.data:
        text = 'В наш бот встроен AI-помощник ✨<b>food2mood✨ - нейросеть персональных рекомендаций еды под настроение!</b> 🍤🍝'
        'Заполни быструю анкету по своему состоянию и вкусовым предпочтениям, а мы подскажем, <b>на какие блюда стоит обратить внимание</b> именно тебе! 🤗🪄'
        if 'return' not in call.data:
            message_with_anketa = await bot.edit_message_text(chat_id=user,
                                                          message_id=call.message.message_id, text=text,
                                                          parse_mode='HTML')
            db.set_first_message_to_delete(user, message_with_anketa.message_id)
        if 'return' not in call.data:
            message_with_first_anketa = await bot.send_message(chat_id=user, text=questiionnaire.make_the_first_q(user),
                                                           reply_markup=questiionnaire.buttons_for_the_first_q())
            db.set_temp_users_message_id(user, message_with_first_anketa.message_id)
        else:
            await bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=questiionnaire.make_the_first_q(user),
                                   reply_markup=questiionnaire.buttons_for_the_first_q())

    if 'delivery' in call.data:
        phone = db.get_users_phone(user)
        if phone:
            await bot.delete_message(chat_id=user, message_id=call.message.message_id)
            await call.message.answer(text="Спасибо! Теперь вы можете продолжить оформление заказа.",
                                       reply_markup=create_web_app_button())
        else:
            contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            contact_keyboard.add(KeyboardButton("📱 Поделиться контактом", request_contact=True))
            text = (
                "Для продолжения нажмите кнопку «ПОДЕЛИТЬСЯ КОНТАКТОМ», "
                "нам это нужно для передачи вам информации о заказе 👇"
            )
            await bot.delete_message(chat_id=user, message_id=call.message.message_id)
            mes_with_phone = await bot.send_message(chat_id=user, text=text, reply_markup=contact_keyboard)
            db.set_temp_users_message_id(user, mes_with_phone.message_id)
