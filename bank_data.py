import csv
from datetime import datetime

import bank_data


class BankData:
    PIN = "1224"
    def __init__(self):
        self.saving_amount = 0.0
        self.checking_amount = 0.0
        self.saving_history = []
        self.checking_history = []

    def validate_pin(self, pin):
        if self.__pin == pin:
            return True
    def reset_pin(self, pin):
        self.__pin = pin

    def deposit_to_saving(self, amount):
        self.saving_amount += amount
        self.saving_history.append((datetime.now(), amount))

    def withdraw_from_saving(self, amount):
        self.saving_amount -= amount
        self.saving_history.append((datetime.now(), -amount))

    def deposit_to_checking(self, amount):
        self.checking_amount += amount
        self.checking_history.append((datetime.now(), amount))

    def withdraw_from_checking(self, amount):
        self.checking_amount -= amount
        self.checking_history.append((datetime.now(), -amount))

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Type', 'Date', 'Amount'])

            for date, amount in self.saving_history:
                writer.writerow(['Saving', date.strftime('%Y-%m-%d %H:%M:%S'), amount])

            for date, amount in self.checking_history:
                writer.writerow(['Checking', date.strftime('%Y-%m-%d %H:%M:%S'), amount])
