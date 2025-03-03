import decimal

from app.src.account.Account import Account
from app.src.banking_agency.IBankingAgencyRepository import IBankingAgencyRepository


class BankingAgencyRepository(IBankingAgencyRepository):
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    async def reset_accounts(self) -> None:
        self.accounts = {}

    async def create_account(self, code, amount) -> decimal.Decimal:
        self.accounts[code] = Account(code, amount)
        return await self.get_account_balance(code)

    async def deposit_account(self, code, amount) -> decimal.Decimal:
        if not await self.check_account_exists(code):
            await self.create_account(code, 0)

        account = self.accounts.get(code)
        return account.deposit(amount)

    async def withdraw_account(self, code, amount)  -> decimal.Decimal:
        account = self.accounts.get(code)
        return account.withdraw(amount)

    async def transfer_account(self, code, amount, destination)  -> decimal.Decimal:
        account = self.accounts.get(code)
        account.withdraw(amount)

        if not await self.check_account_exists(destination):
            await self.create_account(destination, 0)

        account = self.accounts.get(destination)
        return account.deposit(amount)

    async def check_account_exists(self, code) -> bool:
        return code in self.accounts.keys()

    async def get_account_balance(self, code) -> decimal.Decimal:
        account = self.accounts.get(code)
        return account.get_balance()




