from models.Account import Account
class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def reset_accounts(self):
        self.accounts = {}

    def create_account(self, code, amount):
        self.accounts[id] = Account(code, amount)

    def deposit_account(self, code, amount):
        self.accounts[code].deposit(amount)

    def withdraw_account(self, code, amount):
        self.accounts[code].withdraw(amount)

    def transfer_account(self, code, amount, destination):
        self.accounts[code].withdraw(amount)

        if not self.check_account_exists(destination):
            self.create_account(destination, 0)

        self.accounts[destination].deposit(amount)
    def check_account_exists(self, code):
        return code in self.accounts




