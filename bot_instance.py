import os

import telebot
from dotenv import load_dotenv
from telebot import apihelper

load_dotenv()


apihelper.API_URL = os.environ['API_URL']

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

moderator_id = int(os.environ['MODERATOR_ID'])