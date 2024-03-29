import os
import random
import time
from datetime import datetime

class Date:
    def __init__(self, month=0, day=0, year=0):
        self.month = month
        self.day = day
        self.year = year

class Account:
    def __init__(self):
        self.acc_no = 0
        self.name = ""
        self.age = 0
        self.address = ""
        self.citizenship = ""
        self.phone = 0.0
        self.acc_type = ""
        self.amt = 0.0
        self.dob = Date()
        self.deposit = Date()
        self.withdraw = Date()

def calculate_age(dob):
    today = datetime.now()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def generate_account_number():
    # Generate a random 11-digit account number
    return random.randint(10**10, 10**11 - 1)

def deposit():
    acc_no = input("Enter your account number: ")
    deposit_amt = float(input("Enter the amount to deposit: $"))
    # Validate account number
    if not is_account_present(acc_no):
        print("Account not found.")
        return
    # Update balance
    update_balance(acc_no, deposit_amt, "deposit")
    print("Deposit successful.")
    print("Account Balance: ", check_balance(acc_no))

def withdraw():
    acc_no = input("Enter your account number: ")
    withdraw_amt = float(input("Enter the amount to withdraw: $"))

    # Validate account number
    if not is_account_present(acc_no):
        print("Account not found.")
        return

    # Update balance if sufficient balance is available
    if check_balance(acc_no) >= withdraw_amt:
        update_balance(acc_no, withdraw_amt, "withdraw")
        print("Withdrawal successful.")
        print("Account Balance: ", check_balance(acc_no))
    else:
        print("Insufficient balance.")

def check_balance(acc_no):
    with open("record.dat", "r") as file:
        for line in file:
            data = line.split()
            if data[0] == acc_no:
                return float(data[9])  # Return the balance

def is_account_present(acc_no):
    with open("record.dat", "r") as file:
        for line in file:
            data = line.split()
            if data[0] == acc_no:
                return True
    return False

def update_balance(acc_no, amount, transaction_type):
    with open("record.dat", "r") as file:
        lines = file.readlines()

    with open("record.dat", "w") as file:
        for line in lines:
            data = line.split()
            if data[0] == acc_no:
                if transaction_type == "deposit":
                    data[9] = str(float(data[9]) + amount)  # Update balance for deposit
                elif transaction_type == "withdraw":
                    data[9] = str(float(data[9]) - amount)  # Update balance for withdrawal
                line = " ".join(data) + "\n"
            file.write(line)

def balance_enquiry():
    acc_no = input("Enter your account number: ")

    # Validate account number
    if not is_account_present(acc_no):
        print("Account not found.")
        return

    balance = check_balance(acc_no)
    print(f"Your current balance: ${balance:.2f}")

def new_acc():
    # Implementation for new_acc function
    add = Account()
    ptr = open("record.dat", "a+")

    # Automatically fetch today's date
    today_date = datetime.now().date()

    # Generate a random 11-digit account number
    add.acc_no = generate_account_number()

    # User input
    add.deposit = Date(today_date.month, today_date.day, today_date.year)

    add.name = input("\nEnter the name: ")
    add.dob = Date(
        *map(int, input("\nEnter the date of birth(mm/dd/yyyy): ").split("/"))
    )

    # Calculate age
    add.age = calculate_age(datetime(add.dob.year, add.dob.month, add.dob.day))

    # Check age eligibility
    if add.age < 18:
        print("Sorry, you are not eligible to open an account as you are under 18 years old.")
        return

    add.address = input("\nEnter the address: ")
    add.citizenship = input("\nEnter the citizenship number: ")
    add.phone = float(input("\nEnter the phone number: "))
    add.acc_type = input(
        "\nType of account:\n\t1. Saving\n\t2. Current\n\t3. Fixed Deposit\n\t4. Recurring Deposit\n\n\tEnter your choice: "
    )

    # Based on account type, additional options are provided
    if add.acc_type == "1":  # Saving Account
        add.amt = float(input("\nEnter the initial amount to deposit (minimum $100): $"))
        while add.amt < 100:
            print("Minimum deposit amount for a Saving Account is $100.")
            add.amt = float(input("\nEnter the initial amount to deposit (minimum $100): $"))
    elif add.acc_type == "2":  # Current Account
        add.amt = float(input("\nEnter the initial amount to deposit (minimum $500): $"))
        while add.amt < 500:
            print("Minimum deposit amount for a Current Account is $500.")
            add.amt = float(input("\nEnter the initial amount to deposit (minimum $500): $"))
    elif add.acc_type == "3":  # Fixed Deposit
        add.amt = float(input("\nEnter the initial amount to deposit (minimum $100): $"))
        while add.amt < 100:
            print("Minimum deposit amount for a Fixed Deposit is $100.")
            add.amt = float(input("\nEnter the initial amount to deposit (minimum $100): $"))
            add.duration = int(input("\nEnter the duration (in years) for fixed deposit: "))
    elif add.acc_type == "4":  # Recurring Deposit
        add.amt = float(input("\nEnter the initial deposit amount (minimum $100): $"))
        while add.amt < 100:
            print("Minimum initial deposit amount for a Recurring Deposit is $100.")
            add.amt = float(input("\nEnter the initial deposit amount (minimum $100): $"))
            add.duration = int(input("\nEnter the duration (in months) for recurring deposit: "))
    # Write data to file
    ptr.write(
        f"{add.acc_no} {add.name} {add.dob.month}/{add.dob.day}/{add.dob.year} {add.age} {add.address} {add.citizenship} {add.phone} {add.acc_type} {add.amt} {add.deposit.month}/{add.deposit.day}/{add.deposit.year}\n"
    )

    ptr.close()
    print("\nAccount created successfully!")
    # Print account details
    print("\nAccount Details:")
    print("Account Number:", add.acc_no)
    print("Name:", add.name)
    print("Date of Birth:", f"{add.dob.month}/{add.dob.day}/{add.dob.year}")
    print("Age:", add.age)
    print("Address:", add.address)
    print("Citizenship Number:", add.citizenship)
    print("Phone Number:", add.phone)
    print("Account Type:", add.acc_type)
    if add.acc_type in ["3", "4"]:  # Fixed Deposit or Recurring Deposit
        print("Initial Deposit:", f"${add.amt}")
        print("Deposit Date:", f"{add.deposit.month}/{add.deposit.day}/{add.deposit.year}")
        if add.acc_type == "3":  # Fixed Deposit
            print("Duration:", f"{add.duration} years")
        elif add.acc_type == "4":  # Recurring Deposit
            print("Duration:", f"{add.duration} months")
    elif add.acc_type == "2":  # Current Account
        print("Initial Balance:", f"${add.amt}")
    elif add.acc_type == "1":  # Saving Account
        print("Initial Deposit:", f"${add.amt}")
        print("Deposit Date:", f"{add.deposit.month}/{add.deposit.day}/{add.deposit.year}")
    while True:
        choice = input("\nDo you want to continue? (Y/N): ").upper()
        if choice == "Y":
            menu()
        elif choice == "N":
            close()
        else:
            print("Invalid choice. Please enter Y or N.")

def view_list():
    # Implementation for view_list function
    view = open("record.dat", "r")
    test = 0
    print("\nACC. NO.\tNAME\t\t\tADDRESS\t\t\tPHONE\n")

    for line in view:
        data = line.split()
        print(
            f"{data[0]}\t {data[1]}\t\t\t{data[6]}\t\t{float(data[8]):.0f}"
        )
        test += 1

    view.close()
    if test == 0:
        os.system("cls")
        print("\nNO RECORDS!!\n")

    view_list_invalid = input("\n\nEnter 1 to go to the main menu and 0 to exit: ")
    if view_list_invalid == "1":
        menu()
    elif view_list_invalid == "0":
        close()
    else:
        print("\nInvalid!\a")
        view_list()

def employee_menu():
    # Implementation for menu function
    os.system("cls")
    print("\t\t\t\tCUSTOMER ACCOUNT BANKING MANAGEMENT SYSTEM")
    print("\n\n\t\t\t\t\tEMPLOYEE MENU\n\t\t1. NEW ACCOUNT\n\t\t2. ALL ACCOUNT HOLDER LIST\n\t\t3. EXIT\n\t\t")
    print("\t\tSelect Your Option (1-3) ")

    choice = input()

    if choice == "1":
        new_acc()
    elif choice == "2":
        view_list()
    elif choice == "3":
        close()
    else:
        print("\n\n\n\n\a\a\aInvalid input! Please enter the correct option.")
        time.sleep(2)
        employee_menu()

def customer_menu():
    # Implementation for customer_menu function
    os.system("cls")
    print("\t\t\t\tCUSTOMER ACCOUNT BANKING MANAGEMENT SYSTEM")
    print("\n\n\t\t\t\t\tCUSTOMER MENU\n\t\t1. NEW ACCOUNT\n\t\t2. DEPOSIT AMOUNT\n\t\t3. WITHDRAW AMOUNT\n\t\t4. BALANCE ENQUIRY\n\t\t5. EXIT\n\t\t")
    print("\t\tSelect Your Option (1-5) ")

    choice = input()

    if choice == "1":
        new_acc()
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        balance_enquiry()
    elif choice == "5":
        close()
    else:
        print("\n\n\n\n\a\a\aInvalid input! Please enter the correct option.")
        time.sleep(2)
        customer_menu()

def close():
    print("\n\n\n\nThis Python Mini Project is developed by Aloukik")
    exit(0)

def menu():
    # Ask if the user is a customer or an employee
    os.system("cls")
    print("\t\t\t\tCUSTOMER ACCOUNT BANKING MANAGEMENT SYSTEM")
    print("\n\n\t\t\t\t\tLOGIN\n\t\t1. Customer\n\t\t2. Employee\n\t\t3. Exit\n\t\t")
    print("\t\tSelect Your Option (1-3) ")

    choice = input()

    if choice == "1":
        customer_menu()
    elif choice == "2":
        employee_menu()
    elif choice == "3":
        close()
    else:
        print("\n\n\n\n\a\a\aInvalid input! Please enter the correct option.")
        time.sleep(2)
        menu()

# Run the main menu
menu()
