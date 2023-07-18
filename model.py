from sqlalchemy import Column, Integer, String, Float, DATE
from dataclasses import dataclass
from utils import db, mm

@dataclass
class Transac:
    from_account: int
    to_account: int
    amount: float

class Account(db.Model):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    balance = Column(Float)

class AccountSchema(mm.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'balance')

account_Schema = AccountSchema()
accounts_Schema = AccountSchema(many=True)

class Transaction(db.Model):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    from_account = Column(Integer)
    to_account = Column(Integer)
    amount = Column(Float)
    date = Column(DATE)

class TransactionSchema(mm.Schema):
    class Meta:
        fields = ('from_account', 'to_account', 'amount', 'date')

transaction_Schema = TransactionSchema()
transactions_Schema = TransactionSchema(many=True)
