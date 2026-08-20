from bot_instance import bot, telebot
from bot_instance import moderator_id

HELP_COMMAND_TEXT = """Как пользоваться ботом:

Используй кнопки снизу экрана - "Получить Мем" пришлёт случайную картинку из базы, "Отправить Мем" подскажет, что делать дальше.

Прислать свой Мем можно просто фоткой, без нажатия кнопки - он попадёт на модерацию, и после одобрения окажется в общей базе.

Нашёл баг или есть идея? Пиши через /feedback.

Пока что возможно загрузить/получить фотографию. В дальнейшем буду улучшать бота и внедрять новые функции"""

ABOUT_COMMAND_TEXT = """Привет! Меня зовут Мухаммед, я автор этого бота.

Я обожаю <b><u>Русские Мемы</u></b> - постоянно делюсь ими с друзьями, кидаю в чаты и просто пересматриваю свою галерею. В какой-то момент понял, что единого места, где собраны именно <b><u>Русские Мемы</u></b>, не существует - и решил сделать такое место сам.

Этого бота я делал не столько для широкой аудитории, сколько для себя: люблю программировать что-то своё, а тут получилось совместить это с другим увлечением.

Пришли фото - после модерации оно попадёт в общую базу. Есть идея или нашёл баг - пиши через /feedback.

Заранее благодарю в развитие культруры <b><u>Русских Мемов</u></b> :)"""

FEEDBACK_COMMAND_TEXT = 'Напиши свою идею или найденный баг сразу после команды, в одном сообщении. Например:\n/feedback было бы круто добавить поиск по тегам'

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, HELP_COMMAND_TEXT)

@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.chat.id, ABOUT_COMMAND_TEXT, parse_mode='HTML')

@bot.message_handler(commands=['feedback'])
def feedback_command(message):
    feedback_text = message.text.split(maxsplit=1)
    if len(feedback_text) < 2:
        bot.send_message(message.chat.id, FEEDBACK_COMMAND_TEXT)
        return
    bot.send_message(moderator_id, f'Фидбек от {message.from_user.id}: {feedback_text[1]}')
    bot.send_message(message.chat.id, 'Спасибо за вклад! Твоё сообщение отправлено модератору')