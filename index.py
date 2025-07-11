import csv
import time
import os
import hashlib

class BankAccount:
    account_counter = 1000  # Static variable

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction(f"Deposited £{amount:.2f}")
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.add_transaction(f"Withdrew £{amount:.2f}")
            return True
        return False

    def set_interest_rate(self, new_rate):
        self.interest_rate = new_rate / 100
        self.add_transaction(f"Interest rate set to {new_rate:.2f}%")

    def calculate_expected_return(self, years):
        if years < 0:
            return None
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
        return [self.account_number, self.owner, self.balance, self.interest_rate, self.username, self.password_hash]

    def add_transaction(self, message):
        timestamp = time.ctime()
        self.transactions.append((timestamp, message))

    def save_transaction_log(self):
        filename = f"transactions_{self.account_number}.csv"
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Description"])
            for ts, desc in self.transactions:
                writer.writerow([ts, desc])
        print(f"[INFO] Saved transactions to {filename}")

    def load_transaction_log(self):
        filename = f"transactions_{self.account_number}.csv"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                reader = csv.reader(f)
                next(reader)
                self.transactions = [(row[0], row[1]) for row in reader]

    def __str__(self):
        return f"Account #{self.account_number} - {self.owner} | Balance: £{self.balance:.2f} | Interest: {self.interest_rate * 100:.2f}%"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def save_accounts_to_csv(accounts, filename="accounts.csv"):
    try:
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Account Number", "Owner", "Balance", "Interest Rate", "Username", "Password Hash"])
            for acc in accounts.values():
                writer.writerow(acc.to_csv_row())
        for acc in accounts.values():
            acc.save_transaction_log()
        print(f"[INFO] Accounts saved to: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"[ERROR] Failed to save accounts: {e}")


def load_accounts_from_csv(filename="accounts.csv"):
    accounts = {}
    if os.path.exists(filename):
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                acc = BankAccount(
                    row["Owner"],
                    float(row["Balance"]),
                    float(row["Interest Rate"]) * 100,
                    row["Username"],
                    row["Password Hash"]
                )
                acc.account_number = int(row["Account Number"])
                acc.load_transaction_log()
                accounts[acc.account_number] = acc
                if acc.account_number >= BankAccount.account_counter:
                    BankAccount.account_counter = acc.account_number + 1
        print(f"[INFO] Loaded {len(accounts)} account(s).")
    return accounts


def authenticate(accounts, username, password):
    for acc in accounts.values():
        if acc.username == username and acc.password_hash == hash_password(password):
            return acc
    return None


def transfer(from_acc, to_acc, amount):
    if from_acc.withdraw(amount):
        to_acc.deposit(amount)
        from_acc.add_transaction(f"Transferred £{amount:.2f} to {to_acc.account_number}")
        to_acc.add_transaction(f"Received £{amount:.2f} from {from_acc.account_number}")
        return True
    return False


def main():
    accounts = load_accounts_from_csv()

    while True:
        print("\nWelcome to Secure Student Bank!")
        print("1. Create account")
        print("2. Login")
        print("3. Save & Exit")

        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter owner's name: ")
            username = input("Choose username: ")
            if any(acc.username == username for acc in accounts.values()):
                print("Username already exists.")
                continue
            password = input("Choose password: ")
            balance = float(input("Initial deposit (£): "))
            rate = float(input("Interest rate (%): "))
            acc = BankAccount(name, balance, rate, username, hash_password(password))
            acc.apply_tiered_interest()
            accounts[acc.account_number] = acc
            print(f"Account created. Number: {acc.account_number}")

        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            acc = authenticate(accounts, username, password)
            if not acc:
                print("Invalid login.")
                continue

            print(f"Logged in as {acc.owner} (#{acc.account_number})")

            while True:
                print("\n1. Deposit")
                print("2. Withdraw")
                print("3. Set interest rate")
                print("4. Calculate return")
                print("5. Show account info")
                print("6. Transfer")
                print("7. Logout")

                action = input("Choose an action: ")

                if action == '1':
                    amount = float(input("Deposit amount: "))
                    if acc.deposit(amount):
                        print("Deposit successful.")
                    else:
                        print("Invalid amount.")

                elif action == '2':
                    amount = float(input("Withdraw amount: "))
                    if acc.withdraw(amount):
                        print("Withdrawal successful.")
                    else:
                        print("Insufficient funds or invalid amount.")

                elif action == '3':
                    new_rate = float(input("New interest rate (%): "))
                    acc.set_interest_rate(new_rate)
                    print("Interest rate updated.")

                elif action == '4':
                    years = int(input("Years to project: "))
                    result = acc.calculate_expected_return(years)
                    if result:
                        print(f"Expected return (after tax): £{result:.2f}")
                    else:
                        print("Invalid input.")

                elif action == '5':
                    print(acc)
                    for ts, msg in acc.transactions:
                        print(f" - {ts}: {msg}")

                elif action == '6':
                    target_id = int(input("Transfer to account #: "))
                    to_acc = accounts.get(target_id)
                    if not to_acc:
                        print("Target account not found.")
                        continue
                    amount = float(input("Amount to transfer: "))
                    if transfer(acc, to_acc, amount):
                        print("Transfer successful.")
                    else:
                        print("Transfer failed.")

                elif action == '7':
                    print("Logged out.")
                    break

                else:
                    print("Invalid option.")

        elif choice == '3':
            save_accounts_to_csv(accounts)
            print("Goodbye!")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
