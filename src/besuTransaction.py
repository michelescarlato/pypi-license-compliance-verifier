import json
from web3 import Web3

# Read JSON file
with open('/home/michelescarlato/gitrepo/pypi-license-compliance-verifier/src/sherlock/dependencies_tree_with_licenses.json') as json_file:
    json_data = json.load(json_file)

# Connect to Hyperledger Besu
besu_url = "http://localhost:8545"
web3 = Web3(Web3.HTTPProvider(besu_url))

if not web3.isConnected():
    raise Exception("Failed to connect to Hyperledger Besu node")

# Account details: TEST ACCOUNT 3  from https://besu.hyperledger.org/private-networks/tutorials/quickstart
account_from = '0xf17f52151EbEF6C7334FAD080c5704D77216b732'
private_key = '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f'

# Prepare transaction data
transaction = {
    'to': '0x0000000000000000000000000000000000000000',  # Null address
    'value': 0,  # Sending 0 Ether
    'gas': 2000000,
    'gasPrice': web3.toWei('20', 'gwei'),
    'nonce': web3.eth.getTransactionCount(account_from),
    'data': web3.toHex(text=json.dumps(json_data))
}

# Sign the transaction
signed_transaction = web3.eth.account.signTransaction(transaction, private_key)

# Send the transaction
tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

# Wait for the transaction to be mined
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

print(f"Transaction successful with hash: {tx_hash.hex()}")
