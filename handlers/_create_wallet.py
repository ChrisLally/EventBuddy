import requests
from dotenv import load_dotenv
load_dotenv()

#sui_wallet_api_url=os.getenv("SUI_WALLET_URL")
SUI_WALLET_API_URL = "http://127.0.0.1:5000/create_wallet"


async def _create_wallet(app, message):
    await message.reply_photo("https://i.ibb.co/61gGT66/1-S-KRFq4-400x400.png")
    await message.reply_text("👋 I'm EventBuddy, your AI ...")
    response = requests.post(SUI_WALLET_API_URL)
    if response.status_code == 200:
        wallet_data = response.json()
        message.reply_text(f"Wallet created successfully!\nAddress: {wallet_data['address']}\nSeed Phrase: {wallet_data['seed_phrase']}")
    else:
        message.reply_text('Failed to create wallet. Please try again later.')


#def get_nft(update: Update, context: CallbackContext) -> None:
#def give_rating(update: Update, context: CallbackContext) -> None:
#
#def get_airdrop(update: Update, context: CallbackContext) -> None:
#def buy_tickets(update: Update, context: CallbackContext) -> None:



