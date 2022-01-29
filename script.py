from web3 import Web3
import requests
import os
from dotenv import load_dotenv
import json
import argparse

load_dotenv()

etherscan_api_key = os.environ["ETHERSCAN_API_KEY"]
eth_node_url = os.environ["ETH_NODE_URL"]

w3 = Web3(Web3.WebsocketProvider(eth_node_url))

parser = argparse.ArgumentParser()
parser.add_argument("contract", help = "The contract address of the NFT to monitor")

def main():
    is_connected = w3.isConnected()
    if not is_connected:
        raise Exception("Issue connection to the blockchain. Make sure you are using your node's websocket url")

    args = parser.parse_args()
    contract_address = args.contract
    if not Web3.isAddress(contract_address):    
        raise Exception("Invalid contract address")

    # print("Fetching contract ABI from etherscan...")
    # abi = json.loads(requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={etherscan_api_key}").text)['result']
    # checksum_contract_address = w3.toChecksumAddress(contract_address)
    # contract = w3.eth.contract(address=checksum_contract_address, abi=abi)

    print("Success. Fetching transactions...")
    transactions = json.loads(requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startBlock=0&endBlock=99999999&page=1&offset=10&sortby=asc&apikey={etherscan_api_key}").text)['result']
    print("Success. Parsing transactions...")

    first_transaction = transactions[0]
    tx_hash = first_transaction['hash']

    tx = w3.eth.get_transaction(tx_hash)
    # abi = json.loads(requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={tx['to']}&apikey={etherscan_api_key}").text)['result']
    # checksum_contract_address = w3.toChecksumAddress(tx['to'])
    # contract = w3.eth.contract(address=checksum_contract_address, abi=abi)
    # func_obj, func_params = contract.decode_function_input(tx)

    # results = contract.decode_function_input(first_transaction['input'])
    print(tx)

if __name__ == '__main__':
    main()