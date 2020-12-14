import time

from blockchain.block import Block


class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.difficulty = 2  # difficulty of our PoW algorithm
        self.create_genesis_block()  # first block in the blockchain

    def create_genesis_block(self):
        genesis_block = Block(index=0, transactions=[], timestamp=time.time(), previous_hash='0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        # tries different values of nonce to get a hash that satisfies the difficulty criteria
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        # check if block_hash is valid hash of block and satisfies the difficulty criteria
        return block_hash.startswith('0' * self.difficulty) and block_hash == block.compute_hash()

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        # add pending transactions to the blockchain
        if not self.unconfirmed_transactions:
            return "Add transactions"
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.__dict__
