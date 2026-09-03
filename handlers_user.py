from bot_instance import bot, telebot
from db import get_random_meme_from_db, send_meme_to_from_db, count_user_memes_today, user_sended_memes

GET_MEME_REPLY = 'Получить Мем'
SEND_MEME_REPLY = 'Отправить Мем'
GET_MY_MEMES_REPLY = 'Мои Мемы'

meme_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
meme_keyboard.add(telebot.types.KeyboardButton(GET_MEME_REPLY))
meme_keyboard.add(telebot.types.KeyboardButton(SEND_MEME_REPLY))
meme_keyboard.add(telebot.types.KeyboardButton(GET_MY_MEMES_REPLY))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет. Отправь или получи рандомный мем', reply_markup=meme_keyboard)

@bot.message_handler(func=lambda m: m.text == GET_MEME_REPLY)
def getRandomMeme(message):
    meme_row = get_random_meme_from_db()
    if meme_row is None:
        bot.send_message(message.chat.id, 'База Данных с Мемами на данный момент пустая.')
        return
    file_id, media_type = meme_row
    if media_type == 'photo':
        bot.send_photo(message.chat.id, file_id)
    elif media_type == 'video':
        bot.send_video(message.chat.id, file_id)
    else:
        bot.send_animation(message.chat.id, file_id)


@bot.message_handler(func=lambda m: m.text == SEND_MEME_REPLY)
def sendMemeButtonAnswer(message):
    bot.send_message(message.chat.id, 'Пришли свой Мем')

# Новый хендлер для получения всех отправленных Мемов пользователем  
@bot.message_handler(func=lambda m: m.text == GET_MY_MEMES_REPLY)
def getAllUserMemesAnswer(message):
    user_id = message.from_user.id
    file_id = user_sended_memes(user_id)
    chunk_size = 10
    if file_id == []:
        bot.send_message(message.chat.id, 'Вы ещё не отправляли свои Мемы')
        return
    else:
        album_items = [(fid, mt) for fid, mt in file_id if mt != 'animation']
        animation = [fid for fid, mt in file_id if mt == 'animation']
        if len(album_items) == 1:
            fid, mt = album_items[0]
            if mt == 'photo':
                bot.send_photo(message.chat.id, fid)
            else:
                bot.send_video(message.chat.id, fid)
        elif len(album_items) > 1:
            for i in range(0, len(album_items), chunk_size):
                chunk = album_items[i:i + chunk_size]
                if len(chunk) == 1:
                    fid, mt = chunk[0]
                    if mt == 'photo':
                        bot.send_photo(message.chat.id, fid)
                    elif mt == 'video':
                        bot.send_video(message.chat.id, fid)
                else:
                    media = [telebot.types.InputMediaPhoto(fid) if mt == 'photo' else telebot.types.InputMediaVideo(fid) for fid, mt in chunk]
                    bot.send_media_group(message.chat.id, media)
        for fid in animation:
            bot.send_animation(message.chat.id, fid)

@bot.message_handler(content_types=['photo', 'video', 'animation'])
def sendMeme(message):
    content_type = message.content_type
    file_id = None
    user_id = message.from_user.id
    user_memes_today = count_user_memes_today(user_id)

    if content_type == 'photo':
        file_id = message.photo[-1].file_id
    elif content_type == 'video':
        if message.video.file_size is None or message.video.file_size > 10 * 1024 * 1024:
            bot.send_message(message.chat.id, 'Не удалось отправить видео - либо оно больше 10 МБ, либо Telegram не передал его размер. Попробуй другое видео.')
            return
        file_id = message.video.file_id
    elif content_type == 'animation':
        if message.animation.file_size is None or message.animation.file_size > 5 * 1024 * 1024:
            bot.send_message(message.chat.id, 'Не удалось отправить GIF - либо она больше 5 МБ, либо Telegram не передал её размер. Попробуй другую гифку.')
            return
        file_id = message.animation.file_id

    if(user_memes_today >= 40):
        bot.send_message(message.chat.id, 'Превышен лимит отправки Мемов. На одного человека - 40 мемов(пока временно)')
        return

    was_added = send_meme_to_from_db(file_id, user_id, content_type)
    if was_added:
        bot.send_message(message.chat.id, 'Мем успешно сохранён. Спасибо за вклад в развитие культуры!)')
    else:
        bot.send_message(message.chat.id, 'Вы отправили один и тот же Мем дважды. Пожалуйста пришлите другой')