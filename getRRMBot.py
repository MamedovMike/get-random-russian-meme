from bot_instance import bot, telebot

import handlers_info

import handlers_user

import handlers_moderation

bot.set_my_commands([
    telebot.types.BotCommand('start', 'Начать'),
    telebot.types.BotCommand('about', 'О боте'),
    telebot.types.BotCommand('help', 'Помощь'),
    telebot.types.BotCommand('feedback', 'Баги/Идеи'),
])
bot.polling(none_stop=True)