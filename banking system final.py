import os
from datetime import date
import hashlib
import matplotlib.pyplot as plt

ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"


# Utility Functions
def read_file(file_name):
    if not os.path.exists(file_name):
        open(file_name, "w").close()
    with open(file_name, "r") as file:
        return [line.strip() for line in file]

def write_file(file_name, data):
    with open(file_name, "a") as file:
        file.write(data + "\n")

def overwrite_file(file_name, data):
    with open(file_name, "w") as file:
        file.writelines(data)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def parse_account_line(line):
    try:
        parts = line.strip().split(",")
        return {
            "account_number": parts[0],
            "name": parts[1],
            "password_hash": parts[2],
            "balance": float(parts[3])
        }
    except (IndexError, ValueError):
        return None

def format_account_line(account):
    return f"{account['account_number']},{account['name']},{account['password_hash']},{account['balance']}"


# Account Management
def create_account():
    account_number = input("Enter Account Number: ")
    name = input("Enter Name: ")
    password = input("Enter Password: ")
    password_hash = hash_password(password)
    balance = input("Enter Initial Deposit Amount: ")

    write_file(ACCOUNTS_FILE, f"{account_number},{name},{password_hash},{balance}")
    print("Account created successfully!")

def validate_login(account_number, password):
    accounts = read_file(ACCOUNTS_FILE)
    password_hash = hash_password(password)

    for account_line in accounts:
        account = parse_account_line(account_line)
        if account and account["account_number"] == account_number and account["password_hash"] == password_hash:
            return account
    return None


# Transactions
def perform_transaction(account, transaction_type, amount, purpose=None):
    accounts = read_file(ACCOUNTS_FILE)
    updated_accounts = []

    for account_line in accounts:
        existing_account = parse_account_line(account_line)
        if existing_account and existing_account["account_number"] == account["account_number"]:
            if transaction_type == "Withdrawal" and existing_account["balance"] < amount:
                print("Insufficient balance.")
                return False
            
            if transaction_type=="Deposit":
                existing_account["balance"] += amount
            if transaction_type=="Withdrawal":
                existing_account["balance"] += amount
            account["balance"] = existing_account["balance"]  # Update the account object
            updated_accounts.append(format_account_line(existing_account))
        else:
            updated_accounts.append(account_line)

    overwrite_file(ACCOUNTS_FILE, [line + "\n" for line in updated_accounts])

    transaction_details = f"{account['account_number']},{transaction_type},{amount},{purpose or ''},{date.today()}"
    write_file(TRANSACTIONS_FILE, transaction_details)
    print(f"{transaction_type} of {amount} successful.")
    return True

def view_mini_statement(account):
    transactions = read_file(TRANSACTIONS_FILE)
    relevant_transactions = [line for line in transactions if line.startswith(account["account_number"])]
    if relevant_transactions:
        print("Last 5 Transactions:")
        for transaction in relevant_transactions[-5:]:
            print(transaction)
    else:
        print("No transactions found.")

def check_balance(account):
    print(f"Your current balance is: {account['balance']:.2f}")

def spend_analysis(account):
    transactions = read_file(TRANSACTIONS_FILE)
    categories = {"Online Shopping": 0, "POS": 0, "ATM": 0}

    for transaction in transactions:
        parts = transaction.split(",")
        if parts[0] == account["account_number"] and parts[1] == "Withdrawal" and parts[3] in categories:
            categories[parts[3]] += float(parts[2])

    plt.bar(categories.keys(), categories.values(), color="green")
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.title("Spend Analysis")
    plt.show()

def currency_conversion():
    print("\nCurrency Conversion")
    print("1. USD to INR")
    print("2. EUR to INR")
    print("3. GBP to INR")
    print("4. Exit")

    rates = {"1": 82.5, "2": 89.7, "3": 101.2}  # Example rates
    choice = input("Enter your choice: ")

    if choice in rates:
        amount = float(input("Enter amount: "))
        converted = amount * rates[choice]
        print(f"Converted amount: {converted:.2f} INR")
    elif choice == "4":
        print("Exiting Currency Conversion.")
    else:
        print("Invalid choice.")

def main():
    while True:
        print("\nBanking System")
        print("1. Create Account")
        print("2. Login")
        print("3. Currency Conversion")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            account_number = input("Enter Account Number: ")
            password = input("Enter Password: ")

            account = validate_login(account_number, password)
            if account:
                print(f"Login successful! Your balance: {account['balance']:.2f}")
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. View Mini Statement")
                    print("5. Spend Analysis")
                    print("6. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        amount = float(input("Enter deposit amount: "))
                        perform_transaction(account, "Deposit", amount)

                    elif user_choice == "2":
                        amount = float(input("Enter withdrawal amount: "))
                        purpose = input("Enter purpose (Online Shopping, POS, ATM): ")
                        perform_transaction(account, "Withdrawal", -amount, purpose)

                    elif user_choice == "3":
                        check_balance(account)

                    elif user_choice == "4":
                        view_mini_statement(account)

                    elif user_choice == "5":
                        spend_analysis(account)

                    elif user_choice == "6":
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid account number or password.")

        elif choice == "3":
            currency_conversion()

        elif choice == "4":
            print("Thank you for using the Banking System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
