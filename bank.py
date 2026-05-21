print("Welcome to the Bank")

transactions = []
username = "Ronald"
password = "1234"

entered_username = input("Enter username: ")
entered_password = input("Enter password: ")

if entered_username == username and entered_password == password:
    print("Login successful!")
else:
    print("Wrong username or password.")
    exit()

try:
    with open("balance.txt", "r") as file:
        balance = float(file.read())
except:
    balance = 1000

while True:

    print("\nMENU")
    print("1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. View Transactions")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":

        print("Balance:", balance)

    elif choice == "2":

        amount = float(input("Enter deposit amount: "))

        balance += amount
        with open("balance.txt", "w") as file:
            file.write(str(balance))
        
        transactions.append(f"Deposited: ${amount}")
        
        with open("transactions.txt", "a") as f:
            f.write(f"Deposited: ${amount}\n")
        
    
        print("Deposit successful.")

    elif choice == "3":

        amount = float(input("Enter withdrawal amount: "))

        if amount <= balance:

            balance -= amount
            with open("balance.txt", "w") as file:
                file.write(str(balance))
            
            
            transactions.append(f"Withdrew: ${amount}")
            with open("transactions.txt", "a") as f:
                f.write(f"Withdrew: ${amount}\n")
            print("Withdrawal successful.")

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

        print("Goodbye")
        break

    else:

        print("Invalid option")