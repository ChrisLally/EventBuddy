import requests
import json
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder

# Configuration
sui_node_url = "https://fullnode.devnet.sui.io"
wallet_address = "YourSuiWalletAddress"
private_key_hex = "YourPrivateKeyHex"

# Create a signing key from the private key
private_key_bytes = bytes.fromhex(private_key_hex)
signing_key = SigningKey(private_key_bytes)

def mint_nft(to_address, token_uri,name,description,image):
    # Construct the payload for the transaction
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sui_moveCall",
        "params": [
            wallet_address,
            "0x2::devnet_nft::mint",
            [to_address, token_uri, name,description,image],
            1000000,
        ]
    }

    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    # Sign the payload
    signed_payload = signing_key.sign(payload_json.encode(), encoder=HexEncoder).signature

    # Create the headers with the signed payload
    headers = {
        "Content-Type": "application/json",
        "Sui-Signature": signed_payload.hex(),
    }

    # Send the transaction to the Sui node
    response = requests.post(sui_node_url, headers=headers, data=payload_json)

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    # Parse the response
    result = response.json()

    return result

# Example usage
to_address = "RecipientSuiAddress"
token_uri = "https://example.com/nft/metadata.json"

receipt = mint_nft(to_address, token_uri)
print(f"Transaction successful: {receipt}")
