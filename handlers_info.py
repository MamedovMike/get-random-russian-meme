from bot_instance import bot, telebot
from bot_instance import moderator_id
# Импортирование таймера чтобы не было ошибки Too Many Requests
import time

from db import users_sended_meme_rating, get_all_contributors

HELP_COMMAND_TEXT = """Как пользоваться ботом:

Используй кнопки снизу экрана - "Получить Мем" пришлёт случайную картинку из базы, "Отправить Мем" подскажет, что делать дальше, "Мои Мемы" отправит тебе все твои отправленные Мемы

Прислать свой Мем можно просто фоткой/видео/гифкой, без нажатия кнопки - он попадёт на модерацию, и после одобрения окажется в общей базе.

Нашёл баг или есть идея? Пиши через /feedback.

Пока что возможно загрузить/получить фотографию/видео/гифки. В дальнейшем буду улучшать бота и внедрять новые функции"""

ABOUT_COMMAND_TEXT = """Привет! Меня зовут Мухаммед, я автор этого бота.

Я обожаю <b><u>Русские Мемы</u></b> - постоянно делюсь ими с друзьями, кидаю в чаты и просто пересматриваю свою галерею. В какой-то момент понял, что единого места, где собраны именно <b><u>Русские Мемы</u></b>, не существует - и решил сделать такое место сам.

Этого бота я делал не столько для широкой аудитории, сколько для себя: люблю программировать что-то своё, а тут получилось совместить это с другим увлечением.

Пришли фото/видео/гифку - после модерации оно попадёт в общую базу. Есть идея или нашёл баг - пиши через /feedback.

Заранее благодарю в развитие культруры <b><u>Русских Мемов</u></b> :)"""

FEEDBACK_COMMAND_TEXT = 'Напиши свою идею или найденный баг сразу после команды, в одном сообщении. Например:\n/feedback было бы круто добавить поиск по тегам'

NOTIFY_UPDATE_TEXT = """Здравствуйте Мои Дорогие Пользователи!

Для начала хочу от всей Души поблагодарить Вас за то, что делитесь своими Мемами и помогаете пополнять нашу общую базу Русских Мемов - без Вас друзья, этого бота просто не существовало бы 🇷🇺❤

А ещё у меня отличные новости - бот обзавёлся новыми обновлениями! А именно:

Кнопка <b>"Мои Мемы"</b> - теперь можно посмотреть все мемы, которые Вы когда-либо отправляли, удобным альбомом!

🏆 Команда <b>/top</b> Топ-10 самых активных Мемщиков, кто отправил больше всего Мемов. Загляните, может Вы там красуетесь! :)

🎬 <b>Видео и гифки</b> - теперь можно слать не только Фото-Мемы, но и Видео-Мемы (до 10 МБ) а также Гифки! (до 5 МБ)

Спасибо, что Вы со мной и вносите свой вклад в развитие культуры Русских Мемов. Обещаю продолжать делать бота лучше и удобнее для всех вас 🙏

Искренне Ваш, Мухаммед ❤

P.S. Бот лёг на некоторое время из-за проблем с сервером. Впредь постараюсь не допускать такого. Надеюсь на Ваше понимание :("""
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

# Хендлер для показа топ 10 пользователей которые отправили больше всего Мемов
@bot.message_handler(commands=['top'])
def top_10_users(message):
    top = users_sended_meme_rating()
    result_lines = []
    if top == []:
        bot.send_message(message.chat.id, 'Топ Пустой')
    else:
        for i, one_top in enumerate(top, start=1):
            if i == 1:
                place = '🥇'
            elif i == 2:
                place = '🥈'
            elif i == 3:
                place = '🥉'
            else:
                place = f'{i}.'
            user_id, memes_count = one_top
            try:
                chat = bot.get_chat(user_id)
                display_name = f'@{chat.username}' if chat.username else chat.first_name
            except Exception:
                display_name = f'Пользователь {user_id}'
            result_lines.append(f'{place} {display_name} - {memes_count} Мем(ов)')

        final_text = '🏆 Топ 10 Мемщиков:\n\n' + '\n'.join(result_lines) + '\n\nСпасибо Всем за вклад в культуру Русских Мемов! 🇷🇺' + '\n\nИскренне Ваш, Мухаммед ❤'
        bot.send_message(message.chat.id, final_text)

@bot.message_handler(commands=['notify_update'])
def notify_users(message):
    if message.from_user.id != moderator_id:
        return
    contributors = get_all_contributors()
    sent_notify_success = 0
    sent_notify_fail = 0
    for one_contributor in contributors:
        user_id = one_contributor[0]
        try:
            bot.send_message(user_id, NOTIFY_UPDATE_TEXT, parse_mode='HTML')
            time.sleep(0.5)
            sent_notify_success += 1
        except Exception:
            sent_notify_fail += 1
    bot.send_message(moderator_id, f'Разослано успешно {sent_notify_success} пользователям. Не удалось разослать - {sent_notify_fail}')
    
