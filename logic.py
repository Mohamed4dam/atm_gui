from PyQt6.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import csv
import accounts
from gui import Ui_MainWindow
from datetime import datetime
import bank_data
from decimal import Decimal


class PinInputDialog(QDialog):
    def __init__(self, parent=None):
        super(PinInputDialog, self).__init__(parent)
        self.setWindowTitle("Mohamed's ATM")

        layout = QVBoxLayout()

        self.label = QLabel("Please enter your PIN number [hint: 1220 + 4]:")
        self.edit = QLineEdit()
        self.button = QPushButton("OK")

        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.accept)

        self.setLayout(layout)

    def get_pin(self):
        return self.edit.text()
class AmountInputDialog(QDialog):
    def __init__(self, parent=None):
        super(AmountInputDialog, self).__init__(parent)
        self.setWindowTitle("Enter Amount")

        layout = QVBoxLayout()

        self.label = QLabel("Please enter the amount:")
        self.edit = QLineEdit()
        self.button = QPushButton("OK")

        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.accept)

        self.setLayout(layout)
    def get_amount(self):
        try:
            amount = Decimal(self.edit.text())
            rounded_amount = amount.quantize(Decimal('0.01'))
            return float(rounded_amount)

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter a positive number.")
class BankAppLogic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = bank_data.BankData()
        self.label_welcome_user.setText(
            f"<html><head/><body><p><span style=\"font-size:18pt;\">Welcome, Mohamed!</span></p></body></html>")
        self.load_balance_data()

        # Connect signals to slots
        self.pushButton_saving_deposite.clicked.connect(self.deposit_to_saving)
        self.pushButton_saving_withdrawl.clicked.connect(self.withdraw_from_saving)
        self.pushButton_checking_deposite.clicked.connect(self.deposit_to_checking)
        self.pushButton_checking_withdrawl.clicked.connect(self.withdraw_from_checking)


    def validate_pin( entered_pin):
        # You may replace this with your own PIN validation logic
        return entered_pin == bank_data.BankData.PIN

    def update_welcome_page(self):
        selected_user = PinInputDialog()
        if selected_user.exec() == QDialog.DialogCode.Accepted:
            if self.validate_pin(selected_user.get_pin()):
                self._pin_validated = True  # Set pin validation to True
            else:
                # Invalid PIN, show an error message
                print("Invalid PIN")

    def load_balance_data(self):
        try:
            self.data.load_from_csv("file1.csv")
            self.update_balance_labels()
        except FileNotFoundError:
            QMessageBox.warning(self, "File Not Found", "Data file not found. Starting with default values.")

    def update_balance_labels(self):
        self.textBrowser_checking_amount.setFontPointSize(18)
        self.textBrowser_checking_amount.setText(f'${self.data.get_checking_balance()}')
        self.textBrowser_saving_amount.setFontPointSize(18)
        self.textBrowser_saving_amount.setText(f'${self.data.get_saving_balance()}')

        checking_history_text = ""
        for entry in self.data.checking_history:
            date_str = entry[0].strftime('%Y-%m-%d %H:%M:%S')
            amount_str = f'${entry[1]:.2f}'
            checking_history_text += f'{date_str} - Amount: {amount_str}\n'

        self.textBrowser_checking_history.setText(checking_history_text)

        saving_history_text = ""
        for entry in self.data.saving_history:
            s_date_str = entry[0].strftime('%Y-%m-%d %H:%M:%S')
            s_amount_str = f'${entry[1]:.2f}'
            saving_history_text += f'{s_date_str} - Amount: {s_amount_str}\n'
        self.textBrowser_saving_history.setText(saving_history_text)



    def save_data(self):
        self.data.save_to_csv("file1.csv")

    def deposit_to_saving(self):
        amount = self.get_transaction_amount()
        if amount > 0:
            self.data.deposit_to_saving(amount)
            self.update_saving_history(amount)
            self.update_balance_labels()
            self.save_data()

    def withdraw_from_saving(self):
        try:
            amount = self.get_transaction_amount()
            saving_balance = float(self.data.get_saving_balance())

            if amount > 0 and saving_balance >= amount:
                self.data.withdraw_from_saving(amount)
                self.update_saving_history(-amount)
                self.update_balance_labels()
                self.save_data()
        except Exception as e:
            print(f"Error: {e}")
    def deposit_to_checking(self):
        amount = self.get_transaction_amount()
        if amount > 0:
            self.data.deposit_to_checking(amount)
            self.update_checking_history(amount)
            self.update_balance_labels()
            self.save_data()
    def withdraw_from_checking(self):
        try:
            amount = self.get_transaction_amount()
            checking_balance = float(self.data.get_checking_balance())

            if amount > 0 and checking_balance >= amount:
                self.data.withdraw_from_checking(amount)
                self.update_checking_history(-amount)
                self.update_balance_labels()
                self.save_data()
        except Exception as e:
            print(f"Error: {e}")


    def get_transaction_amount(self):
        while True:
            try:
                dialog = AmountInputDialog()
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    amount = dialog.get_amount()
                    if amount > 0 and amount < 1008993010126691712:
                        dialog.accept()
                        return amount
                    else:
                        QMessageBox.warning(self, "Invalid Amount", "Amount must be a non-negative number and less than 10 Million.")
                else:
                    # User canceled the dialog
                    dialog.reject()
                    return 0.00
            except Exception as e:
                print(f"Error in get_transaction_amount: {e}")

    def update_saving_history(self, amount):
        current_text = self.textBrowser_saving_amount.toPlainText()
        new_text = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Amount : {amount:.2f}\n Previous: {current_text}"
        self.textBrowser_saving_history.append(new_text)

    def update_checking_history(self, amount):
        current_text = self.textBrowser_checking_amount.toPlainText()
        new_text = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Amount: {amount:.2f}\n Previous: {current_text}"
        print(new_text)
        self.textBrowser_checking_history.append(new_text)


