import json
from web3 import Web3

# Connect to your Besu node
besu_url = "http://localhost:8545"  # Replace with your Besu node URL
web3 = Web3(Web3.HTTPProvider(besu_url))

if not web3.is_connected():
    raise Exception("Failed to connect to Hyperledger Besu node")

print(f"Connected to Besu node at {besu_url}")

# Define your account details
account_from = '0xf17f52151EbEF6C7334FAD080c5704D77216b732'  # Replace with your account address
private_key = '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f'  # Replace with your private key

# Read JSON file from specified path
json_file_path = '/home/michelescarlato/gitrepo/pypi-license-compliance-verifier/src/sherlock/dependencies_tree_with_licenses.json'
with open(json_file_path) as json_file:
    json_data = json.load(json_file)

# Prepare transaction data
transaction = {
    'to': '0x0000000000000000000000000000000000000000',  # Null address
    'value': 0,  # Sending 0 Ether
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei'),  # Specify a reasonable gas price
    'nonce': web3.eth.get_transaction_count(account_from),
    'data': web3.to_hex(text=json.dumps(json_data))
}

# Sign the transaction
signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Wait for the transaction to be mined
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Transaction successful with hash: {tx_hash.hex()}")
