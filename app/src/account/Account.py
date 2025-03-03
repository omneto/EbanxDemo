import decimal

from app.src.account.IAccount import IAccount


class Account(IAccount):
    def __init__(self, code, balance):
        self.code = code
        self.balance = balance

    def withdraw(self, amount) -> decimal.Decimal:
        self.balance -= amount
        return self.get_balance()

    def deposit(self, amount) -> decimal.Decimal:
        self.balance += amount
        return self.get_balance()

    def get_balance(self) -> decimal.Decimal:
        return self.balance