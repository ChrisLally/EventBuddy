import requests
from dotenv import load_dotenv
load_dotenv()
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base58

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

async def _create_wallet(app, message):
    
    await message.reply_text("CREATING WALLET")
    
    wallet_data = generate_sui_wallet()
    await message.reply_text(f"Wallet created successfully!\nAddress: {wallet_data['address']}\nSeed Phrase: {wallet_data['seed_phrase']}")


