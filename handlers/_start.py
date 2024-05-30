from pyrogram.types import (
    MenuButtonCommands,
    BotCommand,
    BotCommandScopeChat,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.helpers import array_chunk
from pyrogram import filters

start_message="""
START MESSAGE
"""

async def send_question(app, chat_id, question_num, question_text, options):
    # Create a list of InlineKeyboardButtons first 
    buttons = [InlineKeyboardButton(opt, callback_data=f"q{question_num}_{opt}") for opt in options]

    # Then create a 2x2 grid using array_chunk
    button_rows = array_chunk(buttons, 2)  
    keyboard = InlineKeyboardMarkup(button_rows)

    await app.send_message(chat_id, f"Question {question_num}:\n{question_text}", reply_markup=keyboard)

async def _start(app, message):
    print("/start called...")
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("reset", "Reset the bot"),
        BotCommand("about", "About the bot"),
        BotCommand("create_wallet", "Create a wallet")

    ]
    await app.set_bot_commands(
        commands,
        scope=BotCommandScopeChat(chat_id=message.chat.id)
    )
    
    await app.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonCommands()
    )
    
    
    #now we will check the database for this chat_id. If it doesn't exists, set transcript_start
    import t_sqlite3
    if_exists = t_sqlite3.getTranscript(message.chat.id)
    if if_exists==None:
        print('transcript does not exist, creating')
        t_sqlite3.setTranscript(message.chat.id,[{"is_user":True,"message":"/start"},{"is_user":False,"message":start_message}])
    else:
        print("transcript already exists")
    await message.reply_photo("https://i.ibb.co/61gGT66/1-S-KRFq4-400x400.png")
    await message.reply_text(start_message)