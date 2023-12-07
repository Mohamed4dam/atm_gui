

class Account:
    def __init__(self, name, balance=0.00):
        self.__account_name = name
        self .__account_balance = balance
        self.set_balance(balance)


    def deposit(self, amount):
        if amount > 0.00:
          self.__account_balance += amount
          return True
        else:
            return False
    def withdraw(self, amount):
        if amount > 0.00 and amount <= self.get_balance():
            self.__account_balance -= amount
            return True
        else:
             return False
    def get_balance(self):
        return self.__account_balance
    def get_name(self):
        return self.__account_name
    def set_balance(self, amount):
        if amount >= 0.00:
         self.__account_balance = amount

    def set_name(self, name):
        self.__account_name = name

    def __str__(self):
        return f'Account name = {self.get_name()}, Account balance = {self.get_balance()}'

class SavingAccount(Account):
        MINIMUM = 0.0
        RATE = .02

        def __init__(self, name):
            super().__init__(name,SavingAccount.MINIMUM)
            self.__deposit_count = 0



        def apply_interest(self):
            if self.__deposit_count > 4:
                self.set_balance( (self.get_balance() * SavingAccount.RATE) +self.get_balance())
                self.__deposit_count = 0


        def deposit(self, amount):
            if super().deposit(amount) == True:
                self.__deposit_count += 1
                self.apply_interest()
                return True
            else:
                return False


        def withdraw(self, amount):
            if amount <= 0.0 or amount > (self.get_balance() - SavingAccount.MINIMUM):
                return False
            else:
                self.set_balance(self.get_balance()  -amount)
                return True

        def __str__(self):
                return  'SAVING ACCOUNT: ' +super().__str__()







