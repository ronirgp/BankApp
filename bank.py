print("Welcome to the Bank")

transactions = []

users = {
    "Ronald": {
        "password": "1234",
        "balance": 1000
    },

    "Maria": {
        "password": "abcd",
        "balance": 2500
    }
}

entered_username = input("Enter username: ")
entered_password = input("Enter password: ")

if entered_username in users:

    if users[entered_username]["password"] == entered_password:

        print("Login successful!")

        balance = users[entered_username]["balance"]

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
    print("==============================")
    choice = input("Choose: ")

    if choice == "1":

        print("\n==============================")
        print(f"Current Balance: ${balance}")
        print("==============================")

    elif choice == "2":

        amount = float(input("Enter deposit amount: "))

        users[entered_username]["balance"] += amount
        balance = users[entered_username]["balance"]

        transactions.append(f"Deposited: ${amount}")

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

            users[entered_username]["balance"] -= amount
            balance = users[entered_username]["balance"]

            transactions.append(f"Withdrew: ${amount}")

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

        print("\nTransactions:")

        if len(transactions) == 0:
            print("No transactions yet.")

        else:
            for item in transactions:
                print(item)

    elif choice == "5":
        

        receiver = input("Enter receiver username: ")
        

        if receiver in users:
            

            amount = float(input("Enter transfer amount: "))
            

            if amount <= balance:
                

                users[entered_username]["balance"] -= amount
                
                users[receiver]["balance"] += amount
                

                balance = users[entered_username]["balance"]

                transactions.append(f"Transferred ${amount} to {receiver}")
                

                with open("transactions.txt", "a") as f:
                    
                    f.write(f"{entered_username} transferred ${amount} to {receiver}\n")
                    

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
            

    elif choice == "6":

        print("Goodbye")
        break

else:

    print("Invalid option")