import datetime
from uuid import uuid4
import asyncio
import time
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
from aiogram.utils.deep_linking import decode_payload
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup, InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from config import dp, bot, db
from start_bot import *
from handlers.message_handlers import *
from order_and_web_app import *
import menu.categories
import menu.card
import order.order
import handlers.admin_categories
import os


load_dotenv()


if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp)
