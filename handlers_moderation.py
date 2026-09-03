from bot_instance import bot, telebot, moderator_id
from db import get_all_memes_from_db, reject_memes_by_ids, approve_all_pending

@bot.message_handler(commands=['pending'])
def getAllMemes(message):
    if message.from_user.id != moderator_id:
        return      
    memes_data = get_all_memes_from_db()
    if memes_data == []:
        bot.send_message(message.chat.id, 'На данный момент нет Мемов на модерацию')
        return 
    for id, file_id, media_type in memes_data:
        if media_type == 'photo':
            bot.send_photo(message.chat.id, file_id, caption=str(id))
        elif media_type == 'video':
            bot.send_video(message.chat.id, file_id, caption=str(id))
        else:
            bot.send_animation(message.chat.id, file_id, caption=str(id))
            
# Новый хендлер
@bot.message_handler(commands=['reject'])
def reject_memes(message):
    if message.from_user.id != moderator_id:
        return    
    moderator_message = message.text
    ids_raw = moderator_message.split()[1:]
    if ids_raw == []:
        bot.send_message(message.chat.id, 'Нужно указать хотя бы один id')
        return        
    try:
        final_reject_ids = [int(one_id) for one_id in ids_raw]
    except ValueError:
        bot.send_message(message.chat.id, 'Строк быть не должно!')
        return
    rejected_count = reject_memes_by_ids(final_reject_ids)
    remaining_memes = len(get_all_memes_from_db())
    if rejected_count == len(final_reject_ids):
        bot.send_message(message.chat.id, f'Отклонены: {final_reject_ids}. Осталось на модерацию: {remaining_memes}')
    else:
        bot.send_message(message.chat.id, 'Написаны неправильные id')

# Новый хендлер
@bot.message_handler(commands=['approve_all'])
def approve_all(message):
    if message.from_user.id != moderator_id:
        return
    approve_all_pending()
    bot.send_message(message.chat.id, 'Все оставшиеся мемы одобрены')