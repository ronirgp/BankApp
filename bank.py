import json 
import hashlib
def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


from datetime import datetime

print("Welcome to the Bank")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

transactions = []

users = {}

with open("users.json", "r") as file:

    users = json.load(file)
        
def save_users():

    with open("users.json", "w") as file:

        json.dump(users, file, indent=4)
    
    print("Saving users...")

    with open("users.txt", "w") as file:
        for username in users:

            password = users[username]["password"]
            balance = users[username]["balance"]

            file.write(f"{username},{password},{balance}\n")

entered_username = input("Enter username: ").strip()
entered_password = input("Enter password: ").strip()

import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (entered_username,)
)

user = cursor.fetchone()

if user:

    username = user[0]
    password = user[1]
    balance = user[2]

    if (
        password == entered_password
        or
        password == hash_password(entered_password)
    ):

        print("Login successful!")
        
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO login_history
            (username, login_time)
            VALUES (?, ?)
            """,
            (
                entered_username,
                login_time
            )
        )

        conn.commit()
        
        # per-user transaction log file
        transaction_file = f"{entered_username}_transactions.txt"

    else:

        print("Wrong password.")
        exit()

else:

    print("User not found.")
    exit()

while True:

    print("\n==============================")
    print("       BANK SYSTEM MENU")
    print("==============================")
    print("1. Show Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Transactions")
    print("5. Transfer Money")
    print("6. Exit")
    print("7. Create New Account")
    print("8. Delete Account")
    print("9. Admin Panel")
    print("10. Search User")
    print("11. Change Password")
    print("==============================")
    
    choice = input("Choose: ")

    if choice == "1":

        print("\n==============================")
        print(f"Current Balance: ${balance}")
        print("==============================")

    elif choice == "2":

        amount = float(input("Enter deposit amount: "))

        balance += amount

        cursor.execute(
            "UPDATE users SET balance = ? WHERE username = ?",
            (balance, entered_username)
        )

        conn.commit()
        
        cursor.execute(
            """
            INSERT INTO transactions
            (username, date, transaction_type, amount, receiver)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                entered_username,
                timestamp,
                "Deposit",
                amount,
                ""
            )
        )

        conn.commit()
        
        transactions.append(f"Deposited: ${amount}")
        with open(transaction_file, "a") as f:

            f.write(f"{timestamp} | Deposited ${amount} | Balance: ${balance}\n")

        print("\n✅ Deposit successful.")
        
        with open("receipt.txt", "w") as receipt:
            
            receipt.write("----- RECEIPT -----\n")
            receipt.write(f"User: {entered_username}\n")
            receipt.write("Transaction: Deposit\n")
            receipt.write(f"Amount: ${amount}\n")
            receipt.write(f"Balance: ${balance}\n")
            receipt.write("-------------------\n")    

    elif choice == "3":

        amount = float(input("Enter withdrawal amount: "))

        if amount <= balance:

            balance -= amount

            cursor.execute(
                "UPDATE users SET balance = ? WHERE username = ?",
                (balance, entered_username)

            )

            conn.commit()
            
            cursor.execute(
                """
                INSERT INTO transactions
                (username, date, transaction_type, amount, receiver)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    entered_username,
                    timestamp,
                    "Withdrawal",
                    amount,
                    ""
                )
            )

            conn.commit()
            
            transactions.append(f"Withdrew: ${amount}")
            
            with open(transaction_file, "a") as f:
                f.write(f"{timestamp} | Withdrew ${amount} | Balance: ${balance}\n")

            print("\n✅ Withdrawal successful.")
            
            with open("receipt.txt", "w") as receipt:
                receipt.write("----- RECEIPT -----\n")
                receipt.write(f"User: {entered_username}\n")
                receipt.write("Transaction: Withdrawal\n")
                receipt.write(f"Amount: ${amount}\n")
                receipt.write(f"Balance: ${balance}\n")
                receipt.write("-------------------\n")
        else:
            print("Insufficient funds.")

    
    elif choice == "4":

        print("\n===== TRANSACTION HISTORY =====")

        cursor.execute(
            """
            SELECT date, transaction_type, amount, receiver
            FROM transactions
            WHERE username = ?
            ORDER BY id
            """,
            (entered_username,)
        )

        history = cursor.fetchall()

        if history:

            for transaction in history:

                date = transaction[0]
                transaction_type = transaction[1]
                amount = transaction[2]
                receiver = transaction[3]

                if receiver == "":

                    print(f"{date} | {transaction_type} | ${amount}")

                else:

                    print(f"{date} | {transaction_type} | ${amount} | To: {receiver}")

        else:

            print("No transactions yet.")

    elif choice == "5":
        

        receiver = input("Enter receiver username: ")
        

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (receiver,)
        )

        user = cursor.fetchone()

        if user:
            

            amount = float(input("Enter transfer amount: "))
            

            if amount <= balance:
                

                balance -= amount

                cursor.execute(
                    "UPDATE users SET balance = ? WHERE username = ?",
                    (balance, entered_username)
                )

                cursor.execute(
                    "SELECT balance FROM users WHERE username = ?",
                    (receiver,)
                )

                receiver_balance = cursor.fetchone()[0]

                receiver_balance += amount

                cursor.execute(
                    "UPDATE users SET balance = ? WHERE username = ?",
                    (receiver_balance, receiver)
                )

                conn.commit()
                
                cursor.execute(
                    """
                    INSERT INTO transactions
                    (username, date, transaction_type, amount, receiver)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        entered_username,
                        timestamp,
                        "Transfer",
                        amount,
                        receiver
                    )
                )

                conn.commit()

                transactions.append(f"Transferred ${amount} to {receiver}")
                

                with open(transaction_file, "a") as f:
                    
                    f.write(f"{timestamp} | {entered_username} transferred ${amount} to {receiver}\n")
                    

                    print("\n✅ Transfer successful.")
                    
                    with open("receipt.txt", "w") as receipt:

                        receipt.write("----- RECEIPT -----\n")
                        receipt.write(f"Sender: {entered_username}\n")
                        receipt.write(f"Receiver: {receiver}\n")
                        receipt.write("Transaction: Transfer\n")
                        receipt.write(f"Amount: ${amount}\n")
                        receipt.write(f"Balance: ${balance}\n")
                        receipt.write("-------------------\n")

            else:
                print("\n❌ Insufficient funds.")
                
        else:
                print("\n❌ User not found.")
            
    elif choice == "7":

        new_username = input("Create username: ")
    
        if new_username in users:

            print("\n❌ Username already exists.")

        else:

            new_password = input("Create password: ")
            hashed_password = hash_password(new_password)

            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?)",
            (
                    new_username,
                    hashed_password,
                    0,
                    created_date
            )
        )

            conn.commit()

            print("\n✅ Account created successfully.")
            
    
    elif choice == "8":

        username_to_delete = input("Enter account username to delete: ")

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username_to_delete,)
        )

        user = cursor.fetchone()

        if user:

            confirm = input("Type YES to confirm deletion: ")

            if confirm == "YES":

                cursor.execute(
                    "DELETE FROM users WHERE username = ?",
                    (username_to_delete,)
                )

                conn.commit()

                print("\n✅ Account deleted successfully.")

            else:

                print("\n❌ Deletion cancelled.")

        else:

            print("\n❌ User not found.")
            

    elif choice == "6":

        print("Goodbye")
        break
    
    elif choice == "9":

        if entered_username == "admin":

            print("\n========================")
            print("      ADMIN PANEL")
            print("========================")

            print("\nRegistered Users:")

            
            
            cursor.execute(
                """
                SELECT username, created_date
                FROM users
                """
            )

            all_users = cursor.fetchall()

            for user in all_users:

                username = user[0]
                created_date = user[1]

                if created_date is None:

                    created_date = "Unknown"

                cursor.execute(
                    """
                    SELECT login_time
                    FROM login_history
                    WHERE username = ?
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (username,)
                )

                login = cursor.fetchone()

                if login:

                    last_login = login[0]

                else:

                    last_login = "Never"
                    
                    cursor.execute(
                        """
                        SELECT balance
                        FROM users
                        WHERE username = ?
                        """,
                        (username,)
                    )

                    balance_result = cursor.fetchone()

                    balance = balance_result[0]

                print(
                    f"{username} | Balance: ${balance} | Created: {created_date} | Last Login: {last_login}"
                )

            cursor.execute("SELECT SUM(balance) FROM users")

            total_money = cursor.fetchone()[0]

            print(f"\nTotal money in bank: ${total_money}")
            
            print("\nRecent Logins:")

            cursor.execute(
                """
                SELECT username, login_time
                FROM login_history
                ORDER BY id DESC
                LIMIT 5
                """
            )

            recent_logins = cursor.fetchall()

            for login in recent_logins:

                print(f"{login[0]} - {login[1]}")

        else:

            print("\n❌ Access denied. Admin only.")
            
    elif choice == "10":

        if entered_username == "admin":

            username_search = input("Enter username: ")

            cursor.execute(
                """
                SELECT username, balance, created_date
                FROM users
                WHERE username = ?
                """,
                (username_search,)
            )

            user = cursor.fetchone()

            if user:

                username = user[0]
                balance = user[1]
                created_date = user[2]

                if created_date is None:

                    created_date = "Unknown"

                cursor.execute(
                    """
                    SELECT login_time
                    FROM login_history
                    WHERE username = ?
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (username,)
                )

                login = cursor.fetchone()

                if login:

                    last_login = login[0]

                else:

                    last_login = "Never"

                print("\n===== USER INFO =====")
                print(f"Username: {username}")
                print(f"Balance: ${balance}")
                print(f"Created: {created_date}")
                print(f"Last Login: {last_login}")

            else:

                print("\n❌ User not found.")

        else:

            print("\n❌ Admin only.")
            
    elif choice == "11":

        current_password = input("Enter current password: ")

        current_password_hash = hash_password(current_password)

        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username = ?
            """,
            (entered_username,)
        )

        stored_password = cursor.fetchone()[0]

        if current_password_hash == stored_password:

            new_password = input("Enter new password: ")

            confirm_password = input("Confirm new password: ")

            if new_password == confirm_password:

                new_password_hash = hash_password(new_password)

                cursor.execute(
                    """
                    UPDATE users
                    SET password = ?
                    WHERE username = ?
                    """,
                    (
                        new_password_hash,
                        entered_username
                    )
                )

                conn.commit()

                print("\n✅ Password changed successfully.")

            else:

                print("\n❌ Passwords do not match.")

        else:

            print("\n❌ Current password is incorrect.")

    else:

        print("Invalid option")