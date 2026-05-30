import sqlite3
import json

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

with open("users.json", "r") as file:
    users = json.load(file)

for username in users:

    password = users[username]["password"]
    balance = users[username]["balance"]

    cursor.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (username, password, balance)
    )

conn.commit()
conn.close()

print("Users imported successfully!")