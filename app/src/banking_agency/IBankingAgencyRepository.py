import decimal
from abc import ABC, abstractmethod

class IBankingAgencyRepository(ABC):
    @abstractmethod
    async def reset_accounts(self) -> None:
        pass

    @abstractmethod
    async def create_account(self, code, amount) -> decimal.Decimal:
        pass

    @abstractmethod
    async def deposit_account(self, code, amount) -> decimal.Decimal:
        pass

    @abstractmethod
    async def withdraw_account(self, code, amount) -> decimal.Decimal:
        pass

    @abstractmethod
    async def transfer_account(self, code, amount, destination) -> decimal.Decimal:
        pass

    @abstractmethod
    async def check_account_exists(self, code) -> bool:
        pass

    @abstractmethod
    async def get_account_balance(self, code) -> decimal.Decimal:
        pass