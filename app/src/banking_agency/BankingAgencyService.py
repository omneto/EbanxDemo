import decimal

from app.src.banking_agency.IBankingAgencyRepository import IBankingAgencyRepository

class BankingAgencyService:
    def __init__(self, banking_agency_repository: IBankingAgencyRepository):
        self.banking_agency_repository = banking_agency_repository

    def validate_deposit_event(self, destination: str, amount: decimal.Decimal) -> None:
        if decimal.Decimal(amount) < decimal.Decimal('1'):
            raise ValueError("Amount is required.")

        if not destination:
            raise ValueError("Destination is required.")

    def validate_withdraw_event(self, origin: str, amount: decimal.Decimal) -> None:
        if decimal.Decimal(amount) < decimal.Decimal('1'):
            raise ValueError("Amount is required.")

        if not origin:
            raise ValueError("Origin is required.")

    def validate_transfer_event(self, origin: str, amount: decimal.Decimal, destination: str) -> None:
        if decimal.Decimal(amount) < decimal.Decimal('1'):
            raise ValueError("Amount is required.")

        if not origin or not destination:
            raise ValueError("Origin and Destination are required.")

    async def reset_accounts(self) -> None:
        await self.banking_agency_repository.reset_accounts()

    async def create_account(self, code, amount) -> decimal.Decimal:
        return await self.banking_agency_repository.create_account(code, amount)

    async def deposit_account(self, code, amount) -> decimal.Decimal:
        return await self.banking_agency_repository.deposit_account(code, amount)

    async def withdraw_account(self, code, amount)  -> decimal.Decimal:
        return await self.banking_agency_repository.withdraw_account(code, amount)

    async def transfer_account(self, code, amount, destination)  -> decimal.Decimal:
        return await self.banking_agency_repository.transfer_account(code, amount, destination)

    async def check_account_exists(self, code) -> bool:
        return await self.banking_agency_repository.check_account_exists(code)

    async def get_account_balance(self, code) -> decimal.Decimal:
        return await self.banking_agency_repository.get_account_balance(code)
