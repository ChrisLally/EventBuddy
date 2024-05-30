from flask import Flask, jsonify
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base58

from sui_python_sdk.wallet import SuiWallet
from sui_python_sdk.provider import SuiJsonRpcProvider
from sui_python_sdk.rpc_tx_data_serializer import RpcTxDataSerializer
from sui_python_sdk.signer_with_provider import SignerWithProvider
from sui_python_sdk.models import TransferObjectTransaction,TransferSuiTransaction,MoveCallTransaction

from bech32 import bech32_encode, convertbits


import bech32
from typing import Dict, Tuple, Any
from coincurve import PrivateKey

SUI_PRIVATE_KEY_PREFIX = 'suiprivkey'
SIGNATURE_FLAG_TO_SCHEME = {
    0x00: 'ed25519',
    # Add other signature schemes if needed
}
SIGNATURE_SCHEME_TO_FLAG = {v: k for k, v in SIGNATURE_FLAG_TO_SCHEME.items()}
PRIVATE_KEY_SIZE = 32

class ParsedKeypair:
    def __init__(self, schema: str, secret_key: bytes):
        self.schema = schema
        self.secret_key = secret_key

def decode_sui_private_key(value: str) -> ParsedKeypair:
    prefix, words = bech32.bech32_decode(value)
    if prefix != SUI_PRIVATE_KEY_PREFIX:
        raise ValueError('invalid private key prefix')
    extended_secret_key = bech32.convertbits(words, 5, 8, False)
    extended_secret_key = bytearray(extended_secret_key)
    secret_key = bytes(extended_secret_key[1:])
    signature_scheme = SIGNATURE_FLAG_TO_SCHEME[extended_secret_key[0]]
    return ParsedKeypair(signature_scheme, secret_key)

def encode_sui_private_key(bytes: bytes, scheme: str) -> str:
    if len(bytes) != PRIVATE_KEY_SIZE:
        raise ValueError('Invalid bytes length')
    flag = SIGNATURE_SCHEME_TO_FLAG[scheme]
    priv_key_bytes = bytearray([flag]) + bytes
    words = bech32.convertbits(priv_key_bytes, 8, 5, True)
    return bech32.bech32_encode(SUI_PRIVATE_KEY_PREFIX, words)



app = Flask(__name__)


def generate_sui_wallet():
    random_wallet = SuiWallet.create_random_wallet()
    print(random_wallet.get_address())
    print(random_wallet.full_private_key)
    parsed_keypair = ParsedKeypair('ed25519',random_wallet.private_key)
    encoded_key = encode_sui_private_key(parsed_keypair.secret_key, parsed_keypair.schema)
    print(encoded_key)
    decoded_keypair = decode_sui_private_key(encoded_key)
    print(decoded_keypair)
    return {
        "address": random_wallet.get_address(),
        "private_key":encoded_key
    }

   
generate_sui_wallet()

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    wallet = generate_sui_wallet()
    return jsonify(wallet), 200

if __name__ == '__main__':
    app.run(debug=True)

