from model import Account, Transaction
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from utils import db

class AccountRepository:
    def get_account(self, id):
        account = Account.query.filter_by(id=id).first()
        return account

    def update_account(self, account):
        db.session.add(account)
        db.session.commit()


class TransactionRepository:
    def create_transaction(self, transaction_obj):
        transaction = Transaction(
            from_account=transaction_obj.from_account,
            to_account=transaction_obj.to_account,
            amount=transaction_obj.amount,
            date=date.today()
        )
        db.session.add(transaction)
        db.session.commit()


    def get_mini_statement(self, account_id):
        transactions = Transaction.query.filter((Transaction.from_account == account_id) | (Transaction.to_account == account_id)).order_by(Transaction.date.desc()).limit(20).all()
        transaction_list = [transaction for transaction in transactions]
        return transaction_list
