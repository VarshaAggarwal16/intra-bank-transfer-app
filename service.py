from repository import AccountRepository, TransactionRepository
from model import Transac

class AccountService:
    def __init__(self):
        self.account_repo = AccountRepository()

    def get_account(self, id: int):
        account = self.account_repo.get_account(id)
        return account

class TransactionService:
    def __init__(self):
        self.account_repo = AccountRepository()
        self.transaction_repo = TransactionRepository()

    def transfer(self, data):
        transaction_obj = Transac(**data)
        if transaction_obj:
            from_account = self.account_repo.get_account(transaction_obj.from_account)
            if from_account:
                to_account = self.account_repo.get_account(transaction_obj.to_account)
                if to_account:
                    from_account_balance = from_account.balance
                    if from_account_balance >= transaction_obj.amount:
                        from_account.balance -= transaction_obj.amount
                        to_account.balance += transaction_obj.amount
                        self.account_repo.update_account(from_account)
                        self.account_repo.update_account(to_account)
                        self.transaction_repo.create_transaction(transaction_obj)
                        return "Successfully transferred"
                    else:
                        return "Insufficient funds"
                else:
                    return {"error": "to_account not found"}
            else:
                return {"error": "from_account not found"}

    def get_mini_statement(self, account_id):
        transactions = self.transaction_repo.get_mini_statement(account_id)
        return transactions
