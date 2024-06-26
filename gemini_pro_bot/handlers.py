import asyncio
from gemini_pro_bot.llm import model, img_model
from google.generativeai.types.generation_types import (
    StopCandidateException,
    BlockedPromptException,
)
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from telegram.error import NetworkError, BadRequest
from telegram.constants import ChatAction, ParseMode
from gemini_pro_bot.html_format import format_message
import PIL.Image as load_image
from io import BytesIO
from stellar_sdk import Keypair
from sui_python_sdk.wallet import SuiWallet
import bech32
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.helpers import array_chunk
import asyncio
from datetime import datetime
import t_sqlite3
import time
import pytz


def generate_stellar_wallet():
    keypair = Keypair.random()
    address = keypair.public_key
    secret = keypair.secret
    print(address,secret)
    return {
        "address": address,
        "private_key": secret #seed phrase?
    }


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

def generate_sui_wallet():
    random_wallet = SuiWallet.create_random_wallet()
    print(random_wallet.get_address())
    print(random_wallet.full_private_key)
    parsed_keypair = ParsedKeypair('ed25519',random_wallet.private_key)
    encoded_key = encode_sui_private_key(parsed_keypair.secret_key, parsed_keypair.schema)
    print("encoded_key",encoded_key)
    decoded_keypair = decode_sui_private_key(encoded_key)
    print(decoded_keypair)
    return {
        "address": random_wallet.get_address(),
        "private_key":encoded_key
    }

def generate_stellar_wallet():
    keypair = Keypair.random()
    address = keypair.public_key
    secret = keypair.secret
    print(address,secret)
    return {
        "address": address,
        "private_key": secret #seed phrase?
    }

def new_chat(context: ContextTypes.DEFAULT_TYPE):
    # Read the text file
    with open('all_you_need_to_say.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    with open('SuiDocs.txt', 'r', encoding='utf-8') as file:
        text2 = file.read()
    # Clean the text by replacing newlines with spaces and stripping leading/trailing spaces
    clean_text = ' '.join(text.split())

    prompt = """
    You are EventBuddy, a friendly and informative event planning assistant. 
    Your purpose is to help users plan and organize events, from small gatherings to large-scale conferences. 
    You can provide suggestions for venues, activities, catering, and more. 
    You are always eager to assist and ensure that every event is a success.
    
    You will respond in this format for events that START on or after the date/time right now:
    * Event Title: X
    - Date & Time: X
    - Locaiton: X
    - Link: X
    (if continued...)
    * Event Title: X
    - Date & Time: X
    - Locaiton: X
    - Link: X
    
    YOU WILL NOT RESPOND WITH RAW JSON - RESPOND WITH A MAX OF 3 RELEVENT EVENTS:
    """
    
    context_final=prompt+clean_text+" | and here is theSui documentation:"+text2+" So, are you ready to help me?"

    # Initialize a new chat using the cleaned text
    context.chat_data["chat"] = model.start_chat(
    history=[
        {
            'role': 'user',
            'parts': [context_final]  # Use the cleaned text here
        },
        {
            'role': 'model',
            'parts': ['Yes, ask away!']  # Model's response
        },
    ])


import asyncio

from datetime import datetime

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    print("START TRIGGERED")
    
    """Send a message when the command /start is issued."""
    user = update.effective_user
     

    #message = f"Hi {user.mention_html()}!\n\nStart sending messages with me to generate a response.\n\nSend /new to start a new chat session."
    message="""Hello, I'm EventBuddy, your friendly and informative event planning assistant for Consensus 2024! (more to come)
    
Ask about any events happening today, or try /create_sui_wallet or /create_stellar_wallet to generate your new wallet.
    
This new wallet will enable you to make verifiable ratings of the events you attend, and will mint your rating as an NFT!

Hacking this week? I know the Sui docs by heart, ask away!
    """
    
    #user_id = update.message.from_user.id
    # Get the current date and time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write user details and the timestamp to log file
    with open('user_log.txt', 'a') as log_file:
        log_file.write(f"{now} - User {user.id} - {user.username} started the chat.\n")

    # Send the greeting message to the user
    # await update.message.reply_html(
    #     message,
    #     # reply_markup=ForceReply(selective=True),
    # )
    #if_exists = t_sqlite3.getTranscript(user_id)
    # if if_exists==None:
    #     print('transcript does not exist, creating')
    #     t_sqlite3.setTranscript(user_id,[{"is_user":True,"message":"/start"},{"is_user":False,"message":message}])
    # else:
    #     print("transcript already exists")
    await update.message.reply_photo("https://i.postimg.cc/prLD22rQ/photo-2024-05-30-00-49-10.jpg")
    await update.message.reply_text(message)
    # await update.message.reply_photo(
    #     "https://i.ibb.co/61gGT66/1-S-KRFq4-400x400.png"
    # )
    #await update.message.reply_text("👋 I'm EventBuddy, your AI ...")



rate_text="Rate this event out of 5! \n/rate_1\n/rate_2\n/rate_3\n/rate_4\n/rate_5"

async def register_cartesi(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    
    reply_message = f"https://testnet.suivision.xyz/object/0x0f548bdd9e6779b1f2a611a4587038ccf034c4e993d25c03389d80f83a6f1a95\nSaturday, June 1 10:00 AM - 5:00 PM @ 2930 E 12th St Austin, Texas\n\nYou are registered for Builder Demo Days hosted by Cartesi!\nAgenda:\n- 11:00 - 12:00 Guests arrive, mingling & networking\n- 12:00 - 12:30 Lunch will be available\n- 12:30 - 1:30 Opening Speeches from the Hosts\n- 1:30 - 4:00 Pitch Competition\n- 4:00 - 5:00 Open Networking\n- 5:00 Event Ends\n\nEach team will have 10 minutes to pitch and 5 minutes for Q&A from the audience!\n\nYou will get your NFT in your SUI wallet soon!\n"+rate_text
    
    await update.message.reply_text(reply_message)
async def rate_1(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = f"You have rated Builder Demo Days a 1/5 - change your rating up to 24h after the event!\n"+rate_text
    await update.message.reply_text(reply_message)

async def rate_2(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = f"You have rated Builder Demo Days a 2/5 - change your rating up to 24h after the event!\n"+rate_text
    await update.message.reply_text(reply_message)

async def rate_3(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = f"You have rated Builder Demo Days a 3/5 - change your rating up to 24h after the event!\n"+rate_text
    await update.message.reply_text(reply_message)

async def rate_4(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = f"You have rated Builder Demo Days a 4/5 - change your rating up to 24h after the event!\n"+rate_text
    await update.message.reply_text(reply_message)

async def rate_5(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = f"https://testnet.suivision.xyz/object/0x8061c50c0de95bc55d8b0dd18827c7259885d495c1e438a4d4ddf5dba79b4305\nYou have rated Builder Demo Days a 5/5 - change your rating up to 24h after the event!\n"+rate_text
    await update.message.reply_text(reply_message)



async def create_sui_wallet(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    #selected_wallet = await select_option(app, message, "Which blockchain?", {'Sui', 'Stellar'})
    #print('selected_wallet IS: ', selected_wallet)
    user_id = update.message.from_user.id

    wallet=generate_sui_wallet()
    
    #await message.reply_text(f"Creating {selected_wallet} wallet!")
    #if selected_wallet == 'Sui':
    #    wallet=generate_sui_wallet()
    #elif selected_wallet == 'Stellar':
    #    wallet=generate_stellar_wallet()
    
    reply_message = f"Sui wallet created! \n Address: {wallet['address']} \n Private Key: {wallet['private_key']}"
    print(wallet)
    #t_sqlite3.setSuiWallet(user_id,wallet["address"],wallet["private_key"])
    
    await update.message.reply_text(reply_message)
   
async def create_stellar_wallet(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    #selected_wallet = await select_option(app, message, "Which blockchain?", {'Sui', 'Stellar'})
    #print('selected_wallet IS: ', selected_wallet)
    user_id = update.message.from_user.id

    wallet=generate_stellar_wallet()
    
    #await message.reply_text(f"Creating {selected_wallet} wallet!")
    #if selected_wallet == 'Sui':
    #    wallet=generate_sui_wallet()
    #elif selected_wallet == 'Stellar':
    #    wallet=generate_stellar_wallet()
    
    reply_message = f"Stellar wallet created! \n Address: {wallet['address']} \n Private Key: {wallet['private_key']}"
    print(wallet)
    t_sqlite3.setStellarPrivateKey(user_id,wallet["address"],wallet["private_key"])
    
    await update.message.reply_text(reply_message)

#async def get_sui_wallet(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
#    user_id=update.message.from_user.id
#    wallet={
#        "address": t_sqlite3.get,
#        "private_key": secret #seed phrase?
#    }
    



async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
Basic commands:
/start - Start the bot
/help - Get help. Shows this message

Chat commands:
/new - Start a new chat session (model will forget previously generated messages)

Send a message to the bot to generate a response.
"""
    await update.message.reply_text(help_text)


async def newchat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a new chat session."""
    init_msg = await update.message.reply_text(
        text="Starting new chat session...",
        reply_to_message_id=update.message.message_id,
    )
    new_chat(context)
    await init_msg.edit_text("New chat session started.")


# Define the function that will handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming text messages from users.

    Checks if a chat session exists for the user, initializes a new session if not.
    Sends the user's message to the chat session to generate a response.
    Streams the response back to the user, handling any errors.
    """
    if context.chat_data.get("chat") is None:
        new_chat(context)
    text = update.message.text
      
    
    init_msg = await update.message.reply_text(
        text="Generating...", reply_to_message_id=update.message.message_id
    )
    await update.message.chat.send_action(ChatAction.TYPING)
    # Generate a response using the text-generation pipeline
    chat = context.chat_data.get("chat")  # Get the chat session for this chat
    response = None
    try:
        response = await chat.send_message_async(
            text, stream=True
        )  # Generate a response
    except StopCandidateException as sce:
        print("Prompt: ", text, " was stopped. User: ", update.message.from_user)
        print(sce)
        await init_msg.edit_text("The model unexpectedly stopped generating.")
        chat.rewind()  # Rewind the chat session to prevent the bot from getting stuck
        return
    except BlockedPromptException as bpe:
        print("Prompt: ", text, " was blocked. User: ", update.message.from_user)
        print(bpe)
        await init_msg.edit_text("Blocked due to safety concerns.")
        if response:
            # Resolve the response to prevent the chat session from getting stuck
            await response.resolve()
        return
    full_plain_message = ""
    # Stream the responses
    async for chunk in response:
        try:
            if chunk.text:
                full_plain_message += chunk.text
                message = format_message(full_plain_message)
                init_msg = await init_msg.edit_text(
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
        except StopCandidateException as sce:
            await init_msg.edit_text("The model unexpectedly stopped generating.")
            chat.rewind()  # Rewind the chat session to prevent the bot from getting stuck
            continue
        except BadRequest:
            await response.resolve()  # Resolve the response to prevent the chat session from getting stuck
            continue
        except NetworkError:
            raise NetworkError(
                "Looks like you're network is down. Please try again later."
            )
        except IndexError:
            await init_msg.reply_text(
                "Some index error occurred. This response is not supported."
            )
            await response.resolve()
            continue
        except Exception as e:
            print(e)
            if chunk.text:
                full_plain_message = chunk.text
                message = format_message(full_plain_message)
                init_msg = await update.message.reply_text(
                    text=message,
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=init_msg.message_id,
                    disable_web_page_preview=True,
                )
        # Sleep for a bit to prevent the bot from getting rate-limited
        await asyncio.sleep(0.1)


async def handle_image(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming images with captions and generate a response."""
    init_msg = await update.message.reply_text(
        text="Generating...", reply_to_message_id=update.message.message_id
    )
    images = update.message.photo
    unique_images: dict = {}
    for img in images:
        file_id = img.file_id[:-7]
        if file_id not in unique_images:
            unique_images[file_id] = img
        elif img.file_size > unique_images[file_id].file_size:
            unique_images[file_id] = img
    file_list = list(unique_images.values())
    file = await file_list[0].get_file()
    a_img = load_image.open(BytesIO(await file.download_as_bytearray()))
    prompt = None
    if update.message.caption:
        prompt = update.message.caption
    else:
        prompt = "Analyse this image and generate response"
    response = await img_model.generate_content_async([prompt, a_img], stream=True)
    full_plain_message = ""
    async for chunk in response:
        try:
            if chunk.text:
                full_plain_message += chunk.text
                message = format_message(full_plain_message)
                init_msg = await init_msg.edit_text(
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
        except StopCandidateException:
            await init_msg.edit_text("The model unexpectedly stopped generating.")
        except BadRequest:
            await response.resolve()
            continue
        except NetworkError:
            raise NetworkError(
                "Looks like you're network is down. Please try again later."
            )
        except IndexError:
            await init_msg.reply_text(
                "Some index error occurred. This response is not supported."
            )
            await response.resolve()
            continue
        except Exception as e:
            print(e)
            if chunk.text:
                full_plain_message = chunk.text
                message = format_message(full_plain_message)
                init_msg = await update.message.reply_text(
                    text=message,
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=init_msg.message_id,
                    disable_web_page_preview=True,
                )
        await asyncio.sleep(0.1)
