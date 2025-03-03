import decimal
from abc import ABC, abstractmethod

class IAccount(ABC):

    @abstractmethod
    def withdraw(self, amount) -> decimal.Decimal:
        pass

    @abstractmethod
    def deposit(self, amount) -> decimal.Decimal:
        pass

    @abstractmethod
    def get_balance(self) -> decimal.Decimal:
        pass