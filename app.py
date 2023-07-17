from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DATE
from flask_marshmallow import Marshmallow
from dataclasses import dataclass
from datetime import date
import time

import pickle, json
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bank.db')

db = SQLAlchemy(app)
mm = Marshmallow(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')   

@app.cli.command("seed")
def seed():
    account1 =  Account(
        id = 111,
        name = "Puneet Goyal",
        email = "PuneetKumarGoyal@gmail.com",
        balance = 10000.90
    )
    account2 = Account(
        id = 222,
        name = "Varsha Agarwal",
        email = "VarshaAggarwal16@gmail.com",
        balance = 20000.50
    )
    db.session.add(account1)
    db.session.add(account2)
    print(f"time is {time.time()}")
    transaction = Transaction(id = 1, 
                              from_account = 111, 
                              to_account = 222, 
                              amount = 100, 
                              date = date.today())
    db.session.add(transaction)
    db.session.commit()
    print('Database seeded.')

@app.cli.command("drop")
def drop():
    db.drop_all()
    db.session.commit()


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

@dataclass
class Transac():
    from_account : int
    to_account : int
    amount : float

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

@app.route('/account/<int:id>/balance')
def getBalance(id: int):
    account = Account.query.filter_by(id=id).first()
    if account:
        return account_Schema.dumps(account)
    else:
        return jsonify("Account is invalid"), 404
    
@app.route('/transfer', methods=["POST"])
def transfer():
    try:
        data = request.get_json()
        transaction_obj = Transac(**data)
        if transaction_obj:
            from_account = Account.query.filter_by(id=transaction_obj.from_account).first()
            if from_account:
                to_account = Account.query.filter_by(id=transaction_obj.to_account).first()
                if to_account:
                    # check the balance in from_account
                    from_account_balance = from_account.balance
                    print(f"Balance from_account {from_account_balance}")
                    if from_account_balance >= transaction_obj.amount:
                        # Execute the transaction
                        # step 1: debit the from_account
                        from_account.balance -= transaction_obj.amount
                        db.session.add(from_account)
                        # step 2: credit the to_account
                        to_account.balance += transaction_obj.amount
                        db.session.add(to_account)
                        # make an entry in the transaction table
                        print(f"making transaction object")
                        transaction = Transaction( from_account = transaction_obj.from_account, 
                                                  to_account = transaction_obj.to_account, 
                                                  amount = transaction_obj.amount, 
                                                  date = date.today())
                        print(f"transaction object is {transaction}")
                        
                        db.session.add(transaction)
                        db.session.commit()
                    else:
                        # Insuffient funds
                        return jsonify("Insufficient funds"), 200
                else:
                    return jsonify({"error": "to_account not found"})
            else:
                return jsonify({"error": "from_account not found"})
        return jsonify("Successfully transferred"), 200
    except:
        return jsonify("Internal server error occurred."), 500


@app.route('/account/<int:account_id>/getMiniStatement', methods=['GET'])
def getMiniStatement(account_id : int):
    if account_id is None:
        return jsonify({'error': 'accountId parameter is required'}), 400

    transactions = Transaction.query.filter((Transaction.from_account == account_id)  | (Transaction.to_account == account_id)).order_by(Transaction.date.desc()).limit(20).all()
    transaction_list = [transaction for transaction in transactions]
    return transactions_Schema.dump(transaction_list)

if __name__ == "__main__":
    app.run(debug=True)