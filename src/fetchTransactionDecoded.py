from web3 import Web3
import json
from hexbytes import HexBytes

# Connect to your Besu node
besu_url = "http://localhost:8545"  # Besu node URL
web3 = Web3(Web3.HTTPProvider(besu_url))

if not web3.is_connected():
    raise Exception("Failed to connect to Hyperledger Besu node")

print(f"Connected to Besu node at {besu_url}")

# Transaction hash
tx_hash = '0x383f0fe2336374dee16b2c0a2e88f9a20cf2d4ee598880c6cc13dce351aea74f'  # Replace with your transaction hash

# Fetch transaction details
transaction = web3.eth.get_transaction(tx_hash)

# Fetch transaction receipt
receipt = web3.eth.get_transaction_receipt(tx_hash)

#print("Transaction Details:")
#print(transaction)

#print("\nTransaction Receipt:")
#print(receipt)

# Decode and print the input data as JSON
input_data = transaction['input']
decoded_input = bytes(HexBytes(input_data)).decode('utf-8')

print("\nDecoded Input Data:")
try:
    # Pretty print the JSON data
    json_data = json.loads(decoded_input)
    print(json.dumps(json_data, indent=4))
except json.JSONDecodeError:
    print("Input data is not valid JSON:")
    print(decoded_input)

