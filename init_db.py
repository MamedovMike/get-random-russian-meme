import sqlite3

database = sqlite3.connect('russian_memes.db')

# Создания курсора для выполнения команд в БД
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS russian_memes (
    id INTEGER PRIMARY KEY,
    file_id TEXT NOT NULL UNIQUE,
    added_by BIGINT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    media_type TEXT DEFAULT 'photo'
)""")

try:
    cursor.execute("ALTER TABLE russian_memes ADD COLUMN media_type TEXT DEFAULT 'photo'")
except sqlite3.OperationalError:
    pass

database.commit()

database.close()