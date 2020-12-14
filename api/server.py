from flask import Flask, request
import json

from blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()


@app.route('/chain', methods=['GET', 'POST'])
def chain():
    if request.method == 'GET':
        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({
            'length': len(chain_data),
            'chain': chain_data,
        })
    if request.method == 'POST':
        return blockchain.mine()


@app.route('/transactions', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return json.dumps(blockchain.unconfirmed_transactions)
    if request.method == 'POST':
        if not request.form:
            return "Enter transaction data"
        if 'transaction' not in request.form:
            return "Enter transaction data"
        blockchain.add_new_transaction(transaction=request.form.get('transaction'))
        return "added"


def start_server():
    app.run(debug=True, port=5000)
