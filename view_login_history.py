import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM login_history"
)

history = cursor.fetchall()

for row in history:
    print(row)

conn.close()