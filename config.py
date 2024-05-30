from pyrogram import Client
import os, sqlite3
from dotenv import load_dotenv
load_dotenv()

#api_id = os.getenv("APP_ID")
#api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
#sui_wallet_api_url=os.getenv("SUI_WALLET_URL")

app = Client(
    "my_bot",
   # api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
    #sui_wallet_api_url=sui_wallet_api_url
)

conn = sqlite3.connect('bot/database/eventbuddy_db.sqlite')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS eventbuddy (
    address TEXT PRIMARY KEY,
    transcript TEXT,
    privatekey TEXT,
    last_message_timestamp DATETIME
)''')

conn.commit()


app.run()
