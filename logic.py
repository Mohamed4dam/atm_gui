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
    user_checking_acc = accounts.Account('Mohamed', 0.00)
    user_saving_acc = accounts.Account('Mohamed', 100)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = bank_data.BankData()
        self.label_welcome_user.setText(
            f"<html><head/><body><p><span style=\"font-size:12pt;\">Welcome, Mohamed! You got $100 from an anonymous "
            f"account!</span></p></body></html>")

        # Connect signals to slots
        self.pushButton_saving_deposite.clicked.connect(self.deposit_to_saving)
        self.pushButton_saving_withdrawl.clicked.connect(self.withdraw_from_saving)
        self.pushButton_checking_deposite.clicked.connect(self.deposit_to_checking)
        self.pushButton_checking_withdrawl.clicked.connect(self.withdraw_from_checking)

    @staticmethod
    def validate_pin(entered_pin):
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


    def deposit_to_saving(self):
        amount = self.get_transaction_amount()
        if amount > 0:
            self.user_saving_acc.deposit(amount)
            self.update_saving_history(amount)
            self.textBrowser_saving_amount.setFontPointSize(18)
            self.textBrowser_saving_amount.setText(f'${self.user_saving_acc.get_balance()}')

    def withdraw_from_saving(self):
        amount = self.get_transaction_amount()
        if amount > 0:
            self.user_saving_acc.withdraw(amount)
            self.update_saving_history(-amount)
            self.textBrowser_saving_amount.setFontPointSize(18)
            self.textBrowser_saving_amount.setText(f'${self.user_saving_acc.get_balance()}')

    def deposit_to_checking(self):
        amount = self.get_transaction_amount()
        if amount > 0:
            self.user_checking_acc.deposit(amount)
            self.update_checking_history(amount)
            self.textBrowser_checking_amount.setFontPointSize(18)
            self.textBrowser_checking_amount.setText(f'${self.user_checking_acc.get_balance()}')

    def withdraw_from_checking(self):
        amount = self.get_transaction_amount()
        if amount > 0:
            self.user_checking_acc.withdraw(amount)
            self.update_checking_history(-amount)
            self.textBrowser_checking_amount.setFontPointSize(18)
            self.textBrowser_checking_amount.setText(f'${self.user_checking_acc.get_balance()}')


    def get_transaction_amount(self):
        while True:
            try:
                dialog = AmountInputDialog()
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    amount = dialog.get_amount()
                    if amount >= 0:
                        dialog.accept()
                        return amount
                    else:
                        QMessageBox.warning(self, "Invalid Amount", "Amount must be a non-negative number.")
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

    def disable_buttons(self):
        if self.user_saving_acc.get_balance() <= 0:
            self.pushButton_saving_withdrawl.setDisabled(True)
        if self.user_checking_acc.get_balance() <=0:
            self.pushButton_checking_withdrawl.setDisabled(True)
        else:
            self.pushButton_checking_withdrawl.setEnabled(True)

    def save_to_csv(self, filename):
        self.data.save_to_csv(filename)


