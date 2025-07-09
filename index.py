class BankAccount:
    account_counter = 1000  # Static variable to auto-generate account numbers

    def __init__(self, owner, balance, interest_rate):
        self.owner = owner
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.balance = balance
        self.interest_rate = interest_rate / 100  # Store as decimal
        self.transactions = []

    def __str__(self):
        return f"Account #{self.account_number} - Owner: {self.owner}, Balance: £{self.balance:.2f}, Interest Rate: {self.interest_rate * 100:.2f}%"
    

def deposit(account, amount):
    if amount > 0:
        account.balance += amount
        account.transactions.append(f"Deposited £{amount:.2f}")
        print("Deposit successful.")
    else:
        print("Deposit amount must be positive.")

def withdraw(account, amount):
    if amount > 0:
        if account.balance >= amount:
            account.balance -= amount
            account.transactions.append(f"Withdrew £{amount:.2f}")
            print("Withdrawal successful.")
        else:
            print("Insufficient funds.")
    else:
        print("Withdrawal amount must be positive.")


def set_interest_rate(account, new_rate):
    account.interest_rate = new_rate / 100
    account.transactions.append(f"Interest rate set to {new_rate:.2f}%")

def calculate_expected_return(account, years):
    if years < 0:
        print("Number of years must be positive.")
        return None
    P = account.balance
    r = account.interest_rate
    A = P * ((1 + r) ** years)
    return A

accounts = {}

def create_account():
    name = input("Enter owner's name: ")
    deposit_amount = float(input("Initial deposit (£): "))
    interest = float(input("Interest rate (%): "))
    account = BankAccount(name, deposit_amount, interest)
    accounts[account.account_number] = account
    print(f"Account created! Your account number is {account.account_number}")

def find_account():
    acc_num = int(input("Enter account number: "))
    return accounts.get(acc_num, None)

def show_account_info(account):
    print(account)
    for txn in account.transactions:
        print(" -", txn)

def main():
    while True:
        print("\nWelcome to Student Bank!")
        print("1. Create account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Set interest rate")
        print("5. Calculate return")
        print("6. Show account info")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            acc = find_account()
            if acc:
                amount = float(input("Deposit amount: "))
                deposit(acc, amount)
            else:
                print("Account not found.")
        elif choice == '3':
            acc = find_account()
            if acc:
                amount = float(input("Withdraw amount: "))
                withdraw(acc, amount)
            else:
                print("Account not found.")
        elif choice == '4':
            acc = find_account()
            if acc:
                new_rate = float(input("New interest rate (%): "))
                set_interest_rate(acc, new_rate)
            else:
                print("Account not found.")
        elif choice == '5':
            acc = find_account()
            if acc:
                years = int(input("Number of years: "))
                future_value = calculate_expected_return(acc, years)
                if future_value:
                    print(f"Expected return after {years} years: £{future_value:.2f}")
            else:
                print("Account not found.")
        elif choice == '6':
            acc = find_account()
            if acc:
                show_account_info(acc)
            else:
                print("Account not found.")
        elif choice == '7':
            print("Thank you for using Student Bank!")
            break
        else:
            print("Invalid option. Try again.")




def transfer(from_acc, to_acc, amount):
    if from_acc.balance >= amount:
        from_acc.balance -= amount
        to_acc.balance += amount
        from_acc.transactions.append(f"Transferred £{amount:.2f} to {to_acc.account_number}")
        to_acc.transactions.append(f"Received £{amount:.2f} from {from_acc.account_number}")
        print("Transfer successful.")
    else:   
        print("Transfer failed: insufficient funds.")


if __name__ == "__main__":
    main()