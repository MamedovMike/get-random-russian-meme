from bot_instance import bot, telebot, moderator_id
from db import get_all_memes_from_db, reject_memes_by_ids, approve_all_pending

@bot.message_handler(commands=['pending'])
def getAllMemes(message):
    if message.from_user.id != moderator_id:
        return
    else:
        memes_data = get_all_memes_from_db()
        if memes_data == []:
            bot.send_message(message.chat.id, 'На данный момент нет Мемов на модерацию')
            return 
        for id, file_id in memes_data:
             bot.send_photo(message.chat.id, file_id, caption=str(id))

# Новый хендлер
@bot.message_handler(commands=['reject'])
def reject_memes(message):
    if message.from_user.id != moderator_id:
        return
    else:
        moderator_message = message.text
        ids_raw = moderator_message.split()[1:]
        if ids_raw == []:
            bot.send_message(message.chat.id, 'Нужно указать хотя бы один id')
            return
        else:
            try:
                final_reject_ids = [int(one_id) for one_id in ids_raw]
            except ValueError:
                bot.send_message(message.chat.id, 'Строк быть не должно!')
                return

        reject_memes_by_ids(final_reject_ids)
        remaining_memes = len(get_all_memes_from_db())
        bot.send_message(message.chat.id, f'Отклонены: {final_reject_ids}. Осталось на модерацию: {remaining_memes}')

# Новый хендлер
@bot.message_handler(commands=['approve_all'])
def approve_all(message):
    if message.from_user.id != moderator_id:
        return
    else:
        approve_all_pending()
        bot.send_message(message.chat.id, 'Все оставшиеся мемы одобрены')