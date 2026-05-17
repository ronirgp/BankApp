balance = 1000

while True:

    print("\nMENU")
    print("1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":

        print("Balance:", balance)

    elif choice == "2":

        amount = float(input("Enter deposit amount: "))

        balance += amount

        print("Deposit successful.")

    elif choice == "3":

        amount = float(input("Enter withdrawal amount: "))

        if amount <= balance:

            balance -= amount

            print("Withdrawal successful.")

        else:

            print("Insufficient funds.")

    elif choice == "4":

        print("Goodbye")
        break

    else:

        print("Invalid option")