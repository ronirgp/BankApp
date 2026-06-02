import sqlite3

conn = sqlite3.connect("bank.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    balance REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    transaction_type TEXT,
    amount REAL,
    receiver TEXT
)
""")

conn.commit()

conn.close()

print("Database created successfully!")