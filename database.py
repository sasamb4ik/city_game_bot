import sqlite3

# Connect to the database (or create it if it doesn't exist)
outer_conn = sqlite3.connect('users.db')
outer_cursor = outer_conn.cursor()

# Create a table for users
outer_conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER,
    username TEXT,
    score INTEGER,
    best_score INTEGER DEFAULT 0
)
''')


def register_user(chat_id, username):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
        data = cursor.fetchone()

        if data:
            cursor.execute('UPDATE users SET score = 0 WHERE chat_id = ?',
                           (chat_id,))
            conn.commit()
            return True, f'Привет, {username}! Ты начал новую игру. Твой текущий счёт: 0.'
        else:
            cursor.execute(
                'INSERT INTO users (chat_id, username, score) VALUES (?, ?, 0)',
                (chat_id, username))
            conn.commit()
            return True, f'Молодец, {username}, ты успешно зарегистрировался и теперь можешь просматривать свой счёт. Твой текущий счёт: 0.'
    except Exception as e:
        print("Ошибка:", e)
    finally:
        conn.close()


def update_score(username, score):
    cursor = outer_conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = cursor.fetchone()
    current_score, best_score = data[3], data[4]
    if score > best_score:
        cursor.execute(
            'UPDATE users SET score = ?, best_score = ? WHERE username = ?',
            (score, score, username))
        outer_conn.commit()
    else:
        cursor.execute('UPDATE users SET score = ? WHERE username = ?',
                       (score, username))
        outer_conn.commit()


def get_score(username):
    cursor = outer_conn.execute('SELECT score FROM users WHERE username = ?',
                                (username,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_best_score(username):
    cursor = outer_conn.execute(
        'SELECT best_score FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    return row[0] if row else None
