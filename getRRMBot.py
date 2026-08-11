# Для чтения .env и .gitiignore
import os

# Для чтения и записи в БД
import sqlite3

# Для работы бота
import telebot
from dotenv import load_dotenv

load_dotenv()

# Инициализация бота
bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
# Идентификатор модератора для проверок мемов
moderator_id = int(os.environ['MODERATOR_ID'])

# --------Функционал получения и отправки мемов-------#

# Начальное сообщение при нажатии /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создание кнопок
    buttons = telebot.types.InlineKeyboardMarkup()
    # Кнопка получения рандомного мема
    buttons.add(telebot.types.InlineKeyboardButton('Получить Рандомный Мем', callback_data='getMeme'))
    # Кнопка отправления мема
    buttons.add(telebot.types.InlineKeyboardButton('Отправить Мем', callback_data='sendMeme'))
    # Приветственное соощение + вывод кнопок
    bot.send_message(message.chat.id, 'Привет. Отправь или получи рандомный мем', reply_markup=buttons)

# Функция(обработчик/слушатель) получения рандомного мема
@bot.callback_query_handler(func=lambda call:call.data == 'getMeme')
# Функция получения рандомного мема
def getRandomMeme(call):
    # Соединение с БД
    connection = sqlite3.connect('russian_memes.db')
    # Для управления/действий (с) БД
    cursor = connection.cursor()
    # Получение file_id рандомного мема с БД
    cursor.execute("""SELECT file_id FROM russian_memes 
    WHERE status='approved' ORDER BY RANDOM() LIMIT 1
""")
    # В переменную сохраняется подходящая строка
    file_id = cursor.fetchone()
    # Закрытие управления с БД
    cursor.close()
    # Закрытие соединения с БД
    connection.close()
    # Условие: если в БД нет картинок где поле будет approved, выводится сообщение о том что Мемов в БД нет
    if file_id is None:
        bot.send_message(call.message.chat.id, 'База Данных с Мемами на данный момент пустая.')
    # В ином случае бот отправит рандомный Мем
    else:
        bot.send_photo(call.message.chat.id, file_id[0])

    bot.answer_callback_query(call.id)

# Функция(обработчик/слушатель) отправления мема
@bot.callback_query_handler(func=lambda call:call.data == 'sendMeme')
# Функция отправки сообщения если была нажата кнопка "Отправить Мем"
def sendMemeButtonAnswer(call):
    # Отправка сообщения
    bot.send_message(call.message.chat.id, 'Пришли свой Мем')

    bot.answer_callback_query(call.id)
# # Функция(обработчик/слушатель) отправления фотографий
@bot.message_handler(content_types=['photo'])
# Функция принятия и обработки фотографий
def sendMeme(message):
    # В переменную записывается file_id фотографии
    img_file_id = message.photo[-1].file_id

    # Соединение с БД
    connection = sqlite3.connect('russian_memes.db')
    # В эту переменную записывается user_id отправителя для Принятия/Отклонения Мема
    user_id = message.from_user.id

    cursor = connection.cursor()
    # Вставка данных в таблицу: file_id изображения и user_id отправителя
    cursor.execute("""INSERT INTO russian_memes (file_id, added_by)
    VALUES (?, ?)""", (img_file_id, user_id))
    cursor.connection.commit()

    cursor.close()
    connection.close()

# ---------------------------------------------------------- #

# --------------Функционал модерации мемов -----------------#

# Инициализация команды /pending для Модерации Мемов. Хендлер/Слушатель/Обработчик
@bot.message_handler(commands=['pending'])
# Функция получения всех Мемов из БД статус которых является 'pending'
def getAllMemes(message):
    # Валидация/Линия Защиты:
    # Если telegram-id пользователя не совпадает с moderator_id, функция завершается через return
    if message.from_user.id != moderator_id:
        return
    # В противном случае выполнится следующая команда:
    else:
        # Подключение к БД
        connection = sqlite3.connect('russian_memes.db')
        # Для управления/действий (с) БД
        cursor = connection.cursor()
        # Выполнение SQL команды
        cursor.execute("""SELECT id, file_id FROM russian_memes 
            WHERE status='pending'
        """)
        # Список всех подходящих строк выполненной после команды сохраняется в переменную
        memes_data = cursor.fetchall()
        # При отсутствии списка выводится сообщение о том что Мемов на модерации нет
        if memes_data == []:
            # Вывод сообщения
            bot.send_message(message.chat.id, 'На данный момент нет Мемов на модерацию')
            return 
        # Цикл по каждой найденной записи из команды. Для каждой отдельной записи создаётся клавиатура
        for id, file_id in memes_data:
            # Для каждой отдельной записи создаётся клавиатура с двумя кнопками
             buttons = telebot.types.InlineKeyboardMarkup()
            # Кпока 'Одобрить ✅'. Его уникальный код - 'approved_' с вшитым id который был получен через SQL команду
             buttons.add(telebot.types.InlineKeyboardButton('Одобрить ✅', callback_data=f'approved_{id}'))
            # Аналогично с кнопкой 'Отклонить ❌' лишь с тем отличием, что его id - 'rejected_'
             buttons.add(telebot.types.InlineKeyboardButton('Отклонить ❌', callback_data=f'rejected_{id}'))
            # Бот отправляет Мем(Фото) вместе с этой клавиатурой
             bot.send_photo(message.chat.id, file_id, reply_markup=buttons)
        # Закрытие соединения с БД
        cursor.close()
        connection.close()

# Хендлер/Слушатель для кнопки 'Одобрить ✅'
@bot.callback_query_handler(func=lambda call:call.data.startswith('approved_'))
# Функция реакции на кнопку 'Одобрить ✅'. В аргументе лежит 'call' который несёт в себе данные о нажатии кнопки
def approve_meme(call):
    # Та же проверка личности как и в функции 'getAllMemes', только через 'call.from_user.id' - тот кто нажал кнопку
    if call.from_user.id != moderator_id:
        return
    else:
        # Здесь строка разбивается по символу "_" и получается к примеру ['approved', 'id'] 
        data = call.data.split('_')
        # Соединение с БД
        connection = sqlite3.connect('russian_memes.db')
        cursor = connection.cursor()
        # Выполнение SQL команды, где из массива подставляюся данные и Мем меняет свой статус
        cursor.execute("""UPDATE russian_memes SET status = ? WHERE id = ?""", (data[0], data[1]))
        # Закрытие соединения 
        cursor.connection.commit()
        cursor.close()
        connection.close()

        bot.answer_callback_query(call.id)
# Хендлер для кнопки 'Отклонить ❌'. Работает по такому же принципу как и Хендлер для кнопки 'Одобрить ✅'  
@bot.callback_query_handler(func=lambda call:call.data.startswith('rejected_'))
def reject_meme(call):
    if call.from_user.id != moderator_id:
        return
    else:
        data = call.data.split('_')

        connection = sqlite3.connect('russian_memes.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE russian_memes SET status = ? WHERE id = ?""", (data[0], data[1]))
        cursor.connection.commit()
        cursor.close()
        connection.close()

        bot.answer_callback_query(call.id)

# ---------------------------------------------------------- #

bot.polling(none_stop=True)