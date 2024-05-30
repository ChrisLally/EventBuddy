# from stellar_sdk import Keypair
# from sui_python_sdk.wallet import SuiWallet
# import bech32
# from pyrogram.types import (
#     InlineKeyboardButton,
#     InlineKeyboardMarkup
# )
# from pyrogram.helpers import array_chunk




# def generate_stellar_wallet():
#     keypair = Keypair.random()
#     address = keypair.public_key
#     secret = keypair.secret
#     print(address,secret)
#     return {
#         "address": address,
#         "seed_phrase": secret
#     }


# SUI_PRIVATE_KEY_PREFIX = 'suiprivkey'
# SIGNATURE_FLAG_TO_SCHEME = {
#     0x00: 'ed25519',
#     # Add other signature schemes if needed
# }
# SIGNATURE_SCHEME_TO_FLAG = {v: k for k, v in SIGNATURE_FLAG_TO_SCHEME.items()}
# PRIVATE_KEY_SIZE = 32

# class ParsedKeypair:
#     def __init__(self, schema: str, secret_key: bytes):
#         self.schema = schema
#         self.secret_key = secret_key

# def decode_sui_private_key(value: str) -> ParsedKeypair:
#     prefix, words = bech32.bech32_decode(value)
#     if prefix != SUI_PRIVATE_KEY_PREFIX:
#         raise ValueError('invalid private key prefix')
#     extended_secret_key = bech32.convertbits(words, 5, 8, False)
#     extended_secret_key = bytearray(extended_secret_key)
#     secret_key = bytes(extended_secret_key[1:])
#     signature_scheme = SIGNATURE_FLAG_TO_SCHEME[extended_secret_key[0]]
#     return ParsedKeypair(signature_scheme, secret_key)

# def encode_sui_private_key(bytes: bytes, scheme: str) -> str:
#     if len(bytes) != PRIVATE_KEY_SIZE:
#         raise ValueError('Invalid bytes length')
#     flag = SIGNATURE_SCHEME_TO_FLAG[scheme]
#     priv_key_bytes = bytearray([flag]) + bytes
#     words = bech32.convertbits(priv_key_bytes, 8, 5, True)
#     return bech32.bech32_encode(SUI_PRIVATE_KEY_PREFIX, words)

# def generate_sui_wallet():
#     random_wallet = SuiWallet.create_random_wallet()
#     print(random_wallet.get_address())
#     print(random_wallet.full_private_key)
#     parsed_keypair = ParsedKeypair('ed25519',random_wallet.private_key)
#     encoded_key = encode_sui_private_key(parsed_keypair.secret_key, parsed_keypair.schema)
#     print("encoded_key",encoded_key)
#     decoded_keypair = decode_sui_private_key(encoded_key)
#     print(decoded_keypair)
#     return {
#         "address": random_wallet.get_address(),
#         "private_key":encoded_key
#     }



# async def select_option(app, message, prompt, options):
#     chat_id=message.chat.id
#     # Create a list of InlineKeyboardButtons first 
#     buttons = [InlineKeyboardButton(opt, callback_data=f"option_{opt}?") for opt in options]

#     # Then create a 2x2 grid using array_chunk
#     button_rows = array_chunk(buttons, 2)  
#     keyboard = InlineKeyboardMarkup(button_rows)

#     await app.send_message(chat_id, f"{prompt}", reply_markup=keyboard)
    
async def _create_wallet(app, message):
    #selected_wallet = await select_option(app, message, "Which blockchain?", {'Sui', 'Stellar'})
    print('selected_wallet IS: ', selected_wallet)


    
    # #await message.reply_text(f"Creating {selected_wallet} wallet!")
    # if selected_wallet == 'Sui':
    #     wallet=generate_sui_wallet()
    # elif selected_wallet == 'Stellar':
    #     wallet=generate_stellar_wallet()
    
    # reply_message = f"{selected_wallet} wallet created! \n Address: {wallet['address']} \n Private Key: {wallet['private_key']}"
    
    # await message.reply_text(reply_message)
    
   
