import os
import requests
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Web3 instance with LAOS node provider
web3 = Web3(Web3.HTTPProvider('https://rpc.klaosnova.laosfoundation.io'))

# Environment variables
private_key = os.getenv('PRIVATE_KEY')

# The contract address exposing collection creation
contract_address = '0x0000000000000000000000000000000000000403'

# The URL of the interface ABI, from GitHub
contract_abi_url = 'https://github.com/freeverseio/laos/blob/main/precompile/evolution-collection-factory/contracts/EvolutionCollectionFactory.json?raw=true'

def main():
    try:
        # Fetching the contract ABI
        response = requests.get(contract_abi_url)
        contract_abi = response.json()

        # Instantiating the contract
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        # Prepare the transaction
        gas_price = web3.eth.gas_price  # Get current gas price
        account = web3.eth.account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)

        # Build the transaction
        transaction = contract.functions.createCollection(account.address).build_transaction({
            'chainId': web3.eth.chain_id,
            'gas': 45000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        # Sign and send the transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        print('Transaction sent. Waiting for confirmation...')

        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print('Transaction confirmed. Collection created in block number:', receipt.blockNumber)

        # Retrieve the contract address from the transaction receipt
        new_collection_event_abi = next((abi for abi in contract_abi if abi.get('name') == 'NewCollection' and abi.get('type') == 'event'), None)
        new_collection_event = next((log for log in receipt['logs'] if log['address'].lower() == contract_address.lower()), None)
        if new_collection_event and new_collection_event_abi:
            decoded_log = web3.codec.decode_log(new_collection_event_abi['inputs'], new_collection_event['data'], new_collection_event['topics'][1:])
            print(f'Contract address: {decoded_log["_collectionAddress"]}')
        else:
            print('New collection event log not found.')
    except Exception as error:
        print('Error:', error)

if __name__ == '__main__':
    main()

