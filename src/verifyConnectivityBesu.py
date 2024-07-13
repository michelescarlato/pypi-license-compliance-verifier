from web3 import Web3

# Connect to your Besu node
besu_url = "http://localhost:8545"  # Besu node URL
web3 = Web3(Web3.HTTPProvider(besu_url))

if web3.is_connected():
    print(f"Connected to Besu node at {besu_url}")
    print(f"Gas price: {web3.eth.gas_price}")
else:
    print(f"Failed to connect to Besu node at {besu_url}")

