from bot_instance import bot, telebot
from db import get_random_meme_from_db, send_meme_to_from_db, count_user_memes_today

GET_MEME_REPLY = 'Получить Мем'
SEND_MEME_REPLY = 'Отправить Мем'

meme_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
meme_keyboard.add(telebot.types.KeyboardButton(GET_MEME_REPLY))
meme_keyboard.add(telebot.types.KeyboardButton(SEND_MEME_REPLY))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет. Отправь или получи рандомный мем', reply_markup=meme_keyboard)

@bot.message_handler(func=lambda m: m.text == GET_MEME_REPLY)
def getRandomMeme(message):
    file_id = get_random_meme_from_db()
    if file_id is None:
        bot.send_message(message.chat.id, 'База Данных с Мемами на данный момент пустая.')
    else:
        bot.send_photo(message.chat.id, file_id[0])

@bot.message_handler(func=lambda m: m.text == SEND_MEME_REPLY)
def sendMemeButtonAnswer(message):
    bot.send_message(message.chat.id, 'Пришли свой Мем')

@bot.message_handler(content_types=['photo'])
def sendMeme(message):
    img_file_id = message.photo[-1].file_id
    user_id = message.from_user.id
    user_memes_today = count_user_memes_today(user_id)
    if(user_memes_today >= 20):
        bot.send_message(message.chat.id, 'Превышен лимит отправки Мемов. На одного человека - 20 мемов(пока временно)')
    else:
        was_added = send_meme_to_from_db(img_file_id, user_id)
        if was_added:
            bot.send_message(message.chat.id, 'Мем успешно сохранён. Спасибо за вклад в развитие культуры!)')
        else:
            bot.send_message(message.chat.id, 'Вы отправили один и тот же Мем дважды. Пожалуйста пришлите другой')