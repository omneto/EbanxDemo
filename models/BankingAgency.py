from models.Account import Account
class BankingAgency:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def reset_accounts(self):
        self.accounts = {}

    def create_account(self, code, amount):
        self.accounts[code] = Account(code, amount)
        return self.get_account_balance(code)

    def deposit_account(self, code, amount):
        if not self.check_account_exists(code):
            self.create_account(code, 0)

        account = self.accounts.get(code)
        return account.deposit(amount)

    def withdraw_account(self, code, amount):
        account = self.accounts.get(code)
        return account.withdraw(amount)

    def transfer_account(self, code, amount, destination):
        account = self.accounts.get(code)
        account.withdraw(amount)

        if not self.check_account_exists(destination):
            self.create_account(destination, 0)

        account = self.accounts.get(destination)
        return account.deposit(amount)

    def check_account_exists(self, code):
        return code in self.accounts.keys()

    def get_account_balance(self, code):
        account = self.accounts.get(code)
        return account.get_balance()




