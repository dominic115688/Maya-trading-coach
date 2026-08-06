import sqlite3

def init_db():
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, sender TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # New table for trade logging
    cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT, 
                        symbol TEXT, 
                        entry_price REAL, 
                        position_size REAL, 
                        trade_type TEXT, 
                        notes TEXT, 
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = sqlite3.connect('trading_coach.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def log_chat(username, sender, message):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chat_history (username, sender, message) VALUES (?, ?, ?)', (username, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(username):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message FROM chat_history WHERE username = ? ORDER BY timestamp ASC",
        (username,)
    )
    history = cursor.fetchall()
    conn.close()
    return history

def clear_chat_history(username):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    import sqlite3

def init_db():
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, sender TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # New table for trade logging
    cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT, 
                        symbol TEXT, 
                        entry_price REAL, 
                        position_size REAL, 
                        trade_type TEXT, 
                        notes TEXT, 
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = sqlite3.connect('trading_coach.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def log_chat(username, sender, message):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chat_history (username, sender, message) VALUES (?, ?, ?)', (username, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(username):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message FROM chat_history WHERE username = ? ORDER BY timestamp ASC",
        (username,)
    )
    history = cursor.fetchall()
    conn.close()
    return history

def clear_chat_history(username):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def log_trade(username, symbol, entry_price, position_size, trade_type, notes):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO trades (username, symbol, entry_price, position_size, trade_type, notes) VALUES (?, ?, ?, ?, ?, ?)',
        (username, symbol, entry_price, position_size, trade_type, notes)
    )
    conn.commit()
    conn.close()

def get_trades(username):
    conn = sqlite3.connect('trading_coach.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT symbol, entry_price, position_size, trade_type, notes, timestamp FROM trades WHERE username = ? ORDER BY timestamp DESC",
        (username,)
    )
    trades = cursor.fetchall()
    conn.close()
    return trades
