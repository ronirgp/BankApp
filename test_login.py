import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

username = "Ronald"

cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)

user = cursor.fetchone()

print(user)

conn.close()