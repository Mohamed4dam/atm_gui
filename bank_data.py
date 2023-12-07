import csv
from datetime import datetime
import accounts

class BankData:
    """Class representing the bank data and account transactions.

    Attributes:
        PIN (str): The default PIN for the bank.
        user_checking_acc (accounts.Account): The checking account for the user.
        user_saving_acc (accounts.Account): The saving account for the user.
        saving_history (list): List to store saving account transactions.
        checking_history (list): List to store checking account transactions.
    """

    PIN: str = "1224"

    def __init__(self):
        """Initialize BankData with default values."""
        self.user_checking_acc = accounts.Account('Mohamed', 0.00)
        self.user_saving_acc = accounts.Account('Mohamed', 0.00)
        self.saving_history = []
        self.checking_history = []

    def get_checking_balance(self) -> str:
        """Get the current balance of the checking account as a string."""
        checking_balance = sum(amount for _, amount in self.checking_history)
        checking_balance_str = f'{checking_balance:.2f}'
        return checking_balance_str

    def get_saving_balance(self) -> str:
        """Get the current balance of the saving account as a string."""
        saving_balance = sum(amount for _, amount in self.saving_history)
        saving_balance_str = f'{saving_balance:.2f}'
        return saving_balance_str

    def reset_pin(self, pin: str):
        """Reset the bank PIN.

        Args:
            pin (str): The new PIN to be set.
        """
        BankData.PIN = pin

    def deposit_to_saving(self, amount: float):
        """Deposit funds to the saving account.

        Args:
            amount (float): The amount to deposit.
        """
        self.user_saving_acc.deposit(amount)
        self.saving_history.append((datetime.now(), amount))

    def withdraw_from_saving(self, amount: float):
        """Withdraw funds from the saving account.

        Args:
            amount (float): The amount to withdraw.
        """
        self.user_saving_acc.withdraw(amount)
        self.saving_history.append((datetime.now(), -amount))

    def deposit_to_checking(self, amount: float):
        """Deposit funds to the checking account.

        Args:
            amount (float): The amount to deposit.
        """
        self.user_checking_acc.deposit(amount)
        self.checking_history.append((datetime.now(), amount))

    def withdraw_from_checking(self, amount: float):
        """Withdraw funds from the checking account.

        Args:
            amount (float): The amount to withdraw.
        """
        self.user_checking_acc.withdraw(amount)
        self.checking_history.append((datetime.now(), -amount))

    def save_to_csv(self, filename: str):
        """Save account transactions to a CSV file.

        Args:
            filename (str): The name of the CSV file.
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Type', 'Date', 'Amount'])

            for date, amount in self.saving_history:
                writer.writerow(['Saving', date.strftime('%Y-%m-%d %H:%M:%S'), amount])

            for date, amount in self.checking_history:
                writer.writerow(['Checking', date.strftime('%Y-%m-%d %H:%M:%S'), amount])

    def load_from_csv(self, filename: str):
        """Load account transactions from a CSV file.

        Args:
            filename (str): The name of the CSV file.
        """
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    transaction_type = row['Type']
                    date = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
                    amount = float(row['Amount'])

                    if transaction_type == 'Saving':
                        self.saving_history.append((date, amount))
                    elif transaction_type == 'Checking':
                        self.checking_history.append((date, amount))

        except FileNotFoundError:
            print("Data file not found. Starting with default values.")
