import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database.setup import initialize_database
from src.utils.auth import hash_password
from datetime import datetime
import sqlite3

# Initialize database
initialize_database()

DB_PATH = "data/db/bank.db"
TRANSACTION_LOG_DIR = "data/transactions"
LOG_DIR = "logs"
RECEIPT_DIR = "logs/receipts"

# Create directories if they don't exist
os.makedirs(TRANSACTION_LOG_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RECEIPT_DIR, exist_ok=True)

print("Welcome to the Bank")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
transactions = []

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

entered_username = input("Enter username: ").strip()
entered_password = input("Enter password: ").strip()

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
        transaction_file = os.path.join(TRANSACTION_LOG_DIR, f"{entered_username}_transactions.txt")

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
    print("12. User Transaction Report")
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
        
        receipt_path = os.path.join(RECEIPT_DIR, "receipt.txt")
        with open(receipt_path, "w") as receipt:
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
            
            receipt_path = os.path.join(RECEIPT_DIR, "receipt.txt")
            with open(receipt_path, "w") as receipt:
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
                
                receipt_path = os.path.join(RECEIPT_DIR, "receipt.txt")
                with open(receipt_path, "w") as receipt:
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
    
        cursor.execute(
            "SELECT username FROM users WHERE username = ?",
            (new_username,)
        )

        if cursor.fetchone():
            print("\n❌ Username already exists.")
        else:
            new_password = input("Create password: ")
            hashed_password_val = hash_password(new_password)
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?)",
                (
                    new_username,
                    hashed_password_val,
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
                created_date = user[1] if user[1] else "Unknown"

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
                last_login = login[0] if login else "Never"
                
                cursor.execute(
                    """
                    SELECT balance
                    FROM users
                    WHERE username = ?
                    """,
                    (username,)
                )

                balance_result = cursor.fetchone()
                user_balance = balance_result[0]

                print(
                    f"{username} | Balance: ${user_balance} | Created: {created_date} | Last Login: {last_login}"
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
                user_balance = user[1]
                created_date = user[2] if user[2] else "Unknown"

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
                last_login = login[0] if login else "Never"

                print("\n===== USER INFO =====")
                print(f"Username: {username}")
                print(f"Balance: ${user_balance}")
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
            
    elif choice == "12":
        report_user = input("Enter username: ")

        cursor.execute(
            """
            SELECT COUNT(*), COALESCE(SUM(amount),0)
            FROM transactions
            WHERE username = ?
            AND transaction_type = 'Deposit'
            """,
            (report_user,)
        )

        deposit_count, total_deposited = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*), COALESCE(SUM(amount),0)
            FROM transactions
            WHERE username = ?
            AND transaction_type = 'Withdrawal'
            """,
            (report_user,)
        )

        withdrawal_count, total_withdrawn = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*), COALESCE(SUM(amount),0)
            FROM transactions
            WHERE username = ?
            AND transaction_type = 'Transfer'
            """,
            (report_user,)
        )

        transfer_count, total_transferred = cursor.fetchone()

        print("\n===== USER TRANSACTION REPORT =====")
        print(f"User: {report_user}")
        print(f"\nDeposits: {deposit_count}")
        print(f"Total Deposited: ${total_deposited}")
        print(f"\nWithdrawals: {withdrawal_count}")
        print(f"Total Withdrawn: ${total_withdrawn}")
        print(f"\nTransfers: {transfer_count}")
        print(f"Total Transferred: ${total_transferred}")

    else:
        print("Invalid option")

conn.close()
