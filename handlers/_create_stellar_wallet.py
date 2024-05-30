from flask import Flask, jsonify
from stellar_sdk import Keypair
def generate_stellar_wallet():
    keypair = Keypair.random()
    address = keypair.public_key
    secret = keypair.secret
    print(address,secret)

generate_stellar_wallet()

async def _create_stellar_wallet():
    await message.reply_text("CREATING WALLET")
    wallet_data = generate_stellar_wallet()
    await message.reply_text(f"Wallet created successfully!\nAddress: {wallet_data['address']}\nSeed Phrase: {wallet_data['seed_phrase']}")


