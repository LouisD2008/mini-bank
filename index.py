import csv
import time
import os

class BankAccount:
    account_counter = 1000  # Static variable

    def __init__(self, owner, balance, interest_rate):
        self.owner = owner
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.balance = balance
        self.interest_rate = interest_rate / 100  # store as decimal
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append((time.ctime(), f"Deposited £{amount:.2f}"))
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transactions.append((time.ctime(), f"Withdrew £{amount:.2f}"))
            return True
        return False

    def set_interest_rate(self, new_rate):
        self.interest_rate = new_rate / 100
        self.transactions.append((time.ctime(), f"Interest rate set to {new_rate:.2f}%"))

    def calculate_expected_return(self, years):
        if years < 0:
            return None
        # Apply tax on returns (20%)
        A = self.balance * ((1 + self.interest_rate) ** years)
        taxed_A = A * 0.8
        return taxed_A

    def apply_tiered_interest(self):
        if self.balance >= 10000:
            self.interest_rate = 0.03
        elif self.balance >= 5000:
            self.interest_rate = 0.02
        else:
            self.interest_rate = 0.01

    def to_csv_row(self):
        return [self.account_number, self.owner, self.balance, self.interest_rate]

    def load_transaction_log(self):
        return self.transactions

    def __str__(self):
        return f"Account #{self.account_number} - {self.owner} | Balance: £{self.balance:.2f} | Interest: {self.interest_rate * 100:.2f}%"


def save_accounts_to_csv(accounts, filename="accounts.csv"):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Account Number", "Owner", "Balance", "Interest Rate"])
        for acc in accounts.values():
            writer.writerow(acc.to_csv_row())


def load_accounts_from_csv(filename="accounts.csv"):
    accounts = {}
    if os.path.exists(filename):
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                acc = BankAccount(row["Owner"], float(row["Balance"]), float(row["Interest Rate"])*100)
                acc.account_number = int(row["Account Number"])
                accounts[acc.account_number] = acc
                if acc.account_number >= BankAccount.account_counter:
                    BankAccount.account_counter = acc.account_number + 1
    return accounts


def transfer(from_acc, to_acc, amount):
    if from_acc.withdraw(amount):
        to_acc.deposit(amount)
        from_acc.transactions.append((time.ctime(), f"Transferred £{amount:.2f} to {to_acc.account_number}"))
        to_acc.transactions.append((time.ctime(), f"Received £{amount:.2f} from {from_acc.account_number}"))
        return True
    return False


def main():
    accounts = load_accounts_from_csv()
    while True:
        print("\nWelcome to Enhanced Student Bank!")
        print("1. Create account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Set interest rate")
        print("5. Calculate return")
        print("6. Show account info")
        print("7. Transfer")
        print("8. Save & Exit")

        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter owner's name: ")
            balance = float(input("Initial deposit (£): "))
            rate = float(input("Interest rate (%): "))
            acc = BankAccount(name, balance, rate)
            acc.apply_tiered_interest()
            accounts[acc.account_number] = acc
            print(f"Account created. Number: {acc.account_number}")

        elif choice in ['2', '3', '4', '5', '6', '7']:
            acc_num = int(input("Enter account number: "))
            acc = accounts.get(acc_num)
            if not acc:
                print("Account not found.")
                continue

            if choice == '2':
                amount = float(input("Deposit amount: "))
                if acc.deposit(amount):
                    print("Deposit successful.")
                else:
                    print("Invalid amount.")

            elif choice == '3':
                amount = float(input("Withdraw amount: "))
                if acc.withdraw(amount):
                    print("Withdrawal successful.")
                else:
                    print("Insufficient funds or invalid amount.")

            elif choice == '4':
                new_rate = float(input("New interest rate (%): "))
                acc.set_interest_rate(new_rate)
                print("Interest rate updated.")

            elif choice == '5':
                years = int(input("Years to project: "))
                result = acc.calculate_expected_return(years)
                if result:
                    print(f"Expected return (after 20% tax): £{result:.2f}")
                else:
                    print("Invalid year input.")

            elif choice == '6':
                print(acc)
                for time_stamp, event in acc.load_transaction_log():
                    print(f" - {time_stamp}: {event}")

            elif choice == '7':
                target = int(input("Transfer to account #: "))
                to_acc = accounts.get(target)
                if not to_acc:
                    print("Target account not found.")
                    continue
                amount = float(input("Amount to transfer: "))
                if transfer(acc, to_acc, amount):
                    print("Transfer successful.")
                else:
                    print("Transfer failed.")

        elif choice == '8':
            save_accounts_to_csv(accounts)
            print("Accounts saved. Goodbye!")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()