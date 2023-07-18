from flask import jsonify, request
from service import AccountService, TransactionService
from utils import app
from model import account_Schema, transactions_Schema

account_service = AccountService()
transaction_service = TransactionService()

@app.route('/account/<int:id>/balance')
def get_balance(id: int):
    account = account_service.get_account(id)
    if account:
        return account_Schema.dumps(account)
    else:
        return jsonify("Account is invalid"), 404

@app.route('/transfer', methods=["POST"])
def transfer():
    try:
        data = request.get_json()
        result = transaction_service.transfer(data)
        if result == "Insufficient funds":
            return jsonify(result), 200
        elif result == "Successfully transferred":
            return jsonify(result), 200
        else:
            return jsonify("Internal server error occurred."), 500
    except:
        return jsonify("Internal server error occurred."), 500

@app.route('/account/<int:account_id>/getMiniStatement', methods=['GET'])
def get_mini_statement(account_id: int):
    if account_id is None:
        return jsonify({'error': 'accountId parameter is required'}), 400

    transactions = transaction_service.get_mini_statement(account_id)
    return transactions_Schema.dump(transactions)

if __name__ == "__main__":
    app.run(debug=True)
