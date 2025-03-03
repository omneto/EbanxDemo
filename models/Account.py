class Account:
    def __init__(self, code, balance):
        self.code = code
        self.balance = balance

    def withdraw(self, amount):
        self.balance -= amount
        return self.get_balance()

    def deposit(self, amount):
        self.balance += amount
        return self.get_balance()

    def get_balance(self):
        return self.balance