import os

import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

moderator_id = int(os.environ['MODERATOR_ID'])