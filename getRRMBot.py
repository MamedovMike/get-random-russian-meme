import os

import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def start(message):
    buttons = telebot.types.InlineKeyboardMarkup()
    buttons.add(telebot.types.InlineKeyboardButton('Получить Рандомный Мем', callback_data='Получить рандомный мем'))
    buttons.add(telebot.types.InlineKeyboardButton('Отправить Мем', callback_data='Отправить мем'))
    bot.send_message(message.chat.id, 'Привет. Отправь или получи рандомный мем', reply_markup=buttons)

# @bot.callback_query_handler(func=lambda call:True)
# def getRandomMeme(call):
    

bot.polling(none_stop=True)