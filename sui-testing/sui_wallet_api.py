from flask import Flask, jsonify
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base58

app = Flask(__name__)

def generate_sui_wallet():
    # Generate a new Ed25519 private key
    private_key = ed25519.Ed25519PrivateKey.generate()
    
    # Get the public key
    public_key = private_key.public_key()
    
    # Serialize keys
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    
    # Encode the public key in base58 for the wallet address
    address = base58.b58encode(public_key_bytes).decode('utf-8')
    
    # Convert private key to seed phrase (this is a simplified example, normally you'd use a BIP39 library)
    seed_phrase = base58.b58encode(private_key_bytes).decode('utf-8')
    
    return {
        "address": address,
        "seed_phrase": seed_phrase
    }

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    wallet = generate_sui_wallet()
    return jsonify(wallet), 200

if __name__ == '__main__':
    app.run(debug=True)

