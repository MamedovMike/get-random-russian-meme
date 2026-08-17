from bot_instance import bot, telebot
from db import get_random_meme_from_db, send_meme_to_from_db

@bot.message_handler(commands=['start'])
def start(message):
    buttons = telebot.types.InlineKeyboardMarkup()
    buttons.add(telebot.types.InlineKeyboardButton('Получить Рандомный Мем', callback_data='getMeme'))
    buttons.add(telebot.types.InlineKeyboardButton('Отправить Мем', callback_data='sendMeme'))
    bot.send_message(message.chat.id, 'Привет. Отправь или получи рандомный мем', reply_markup=buttons)

@bot.callback_query_handler(func=lambda call:call.data == 'getMeme')
def getRandomMeme(call):
    file_id = get_random_meme_from_db()
    if file_id is None:
        bot.send_message(call.message.chat.id, 'База Данных с Мемами на данный момент пустая.')
    else:
        bot.send_photo(call.message.chat.id, file_id[0])

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call:call.data == 'sendMeme')
def sendMemeButtonAnswer(call):
    bot.send_message(call.message.chat.id, 'Пришли свой Мем')

    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def sendMeme(message):
    img_file_id = message.photo[-1].file_id
    user_id = message.from_user.id
    was_added = send_meme_to_from_db(img_file_id, user_id)
    if was_added:
        bot.send_message(message.chat.id, 'Мем успешно сохранён. Спасибо за вклад в развитие культуры!)')
    else:
        bot.send_message(message.chat.id, 'Вы отправили один и тот же Мем дважды. Пожалуйста пришлите другой')