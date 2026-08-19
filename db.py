import sqlite3

def get_random_meme_from_db():
    connection = sqlite3.connect('russian_memes.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT file_id FROM russian_memes 
    WHERE status='approved' ORDER BY RANDOM() LIMIT 1
""")
    meme_row = cursor.fetchone()
    cursor.close()
    connection.close()
    return meme_row

def send_meme_to_from_db(file_id, added_by):
    connection = sqlite3.connect('russian_memes.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO russian_memes (file_id, added_by)
        VALUES (?, ?)""", (file_id, added_by))
        cursor.connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        cursor.close()
        connection.close()


def get_all_memes_from_db():
    connection = sqlite3.connect('russian_memes.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT id, file_id FROM russian_memes 
    WHERE status='pending'
""")
    memes_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return memes_data

# Новая функция - реализация улучшеемя MVP
def reject_memes_by_ids(ids):

    placeholder_list = ['?'] * len(ids)
    placeholders = ', '.join(placeholder_list)

    connection = sqlite3.connect('russian_memes.db')
    cursor = connection.cursor()
    cursor.execute(f"""UPDATE russian_memes SET status ='rejected' WHERE id IN ({placeholders}) AND status='pending'""", (ids))
    cursor.connection.commit()
    cursor.close()
    connection.close()

# Вторая ф-ия, та же реализация
def approve_all_pending():
    connection = sqlite3.connect('russian_memes.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE russian_memes SET status='approved' WHERE status='pending'""")
    cursor.connection.commit()
    cursor.close()
    connection.close()

# Новая функция для проверки сколько Мемов отправил пользователь
def count_user_memes_today(user_id):
    connection = sqlite3.connect('russian_memes.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT COUNT(*) FROM russian_memes WHERE added_by=? AND date(created_at) = date('now')""", (user_id,))
    user_memes_today = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_memes_today[0]