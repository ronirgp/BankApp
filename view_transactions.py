import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM transactions")

for row in cursor.fetchall():

    print(row)

conn.close()