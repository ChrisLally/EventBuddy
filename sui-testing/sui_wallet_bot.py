from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Replace with your actual Sui wallet creation API endpoint
SUI_WALLET_API_URL = "http://127.0.0.1:5000/create_wallet"

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = "6574171342:AAHOl6IzuImM6TLf7984gSiOtct896QwAdU"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Use /create_wallet to create a new Sui wallet.')

def create_wallet(update: Update, context: CallbackContext) -> None:
    response = requests.post(SUI_WALLET_API_URL)
    if response.status_code == 200:
        wallet_data = response.json()
        update.message.reply_text(f"Wallet created successfully!\nAddress: {wallet_data['address']}\nSeed Phrase: {wallet_data['seed_phrase']}")
    else:
        update.message.reply_text('Failed to create wallet. Please try again later.')

def get_nft(update: Update, context: CallbackContext) -> None:
def give_rating(update: Update, context: CallbackContext) -> None:

def get_airdrop(update: Update, context: CallbackContext) -> None:
def buy_tickets(update: Update, context: CallbackContext) -> None:



def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create_wallet", create_wallet))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
