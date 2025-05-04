import sqlite3

conn = sqlite3.connect("jackpot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS entries (
    user_id INTEGER,
    wallet TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)""")

conn.commit()

def add_entry(user_id, wallet):
    cursor.execute("INSERT INTO entries (user_id, wallet) VALUES (?, ?)", (user_id, wallet))
    conn.commit()

def get_entries():
    cursor.execute("SELECT * FROM entries")
    return cursor.fetchall()

def clear_entries():
    cursor.execute("DELETE FROM entries")
    conn.commit()

def set_setting(key, value):
    cursor.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()

def get_setting(key, default=None):
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    return row[0] if row else default
