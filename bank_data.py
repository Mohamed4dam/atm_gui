import csv
from datetime import datetime
import accounts

import bank_data


class BankData:
    PIN = "1224"
    def __init__(self):
        self.user_checking_acc = accounts.Account('Mohamed', 0.00)
        self.user_saving_acc = accounts.Account('Mohamed', 0.00)
        self.saving_history = []
        self.checking_history = []

    def get_checking_balance(self):
        checking_balance = sum(amount for _, amount in self.checking_history)
        checking_balance_str = f'{checking_balance:.2f}'
        return checking_balance_str

    def get_saving_balance(self):
        saving_balance = sum(amount for _, amount in self.saving_history)
        saving_balance_str = f'{saving_balance:.2f}'
        return saving_balance_str


    def reset_pin(self, pin):
        BankData.PIN = pin

    def deposit_to_saving(self, amount):
        self.user_saving_acc.deposit(amount)
        self.saving_history.append((datetime.now(), amount))

    def withdraw_from_saving(self, amount):
        self.user_saving_acc.withdraw(amount)
        self.saving_history.append((datetime.now(), -amount))

    def deposit_to_checking(self, amount):
        self.user_checking_acc.deposit(amount)
        self.checking_history.append((datetime.now(), amount))

    def withdraw_from_checking(self, amount):
        self.user_checking_acc.withdraw(amount)
        self.checking_history.append((datetime.now(), -amount))

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Type', 'Date', 'Amount'])

            for date, amount in self.saving_history:
                writer.writerow(['Saving', date.strftime('%Y-%m-%d %H:%M:%S'), amount])

            for date, amount in self.checking_history:
                writer.writerow(['Checking', date.strftime('%Y-%m-%d %H:%M:%S'), amount])

    def load_from_csv(self, filename):
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



