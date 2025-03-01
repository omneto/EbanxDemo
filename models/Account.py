class Account:
    def __init__(self, code, balance):
        self.id = code
        self.balance = balance

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def balance(self):
        return self.balance