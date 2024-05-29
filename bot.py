from pyrogram import Client, filters, enums

from pyrogram.types import (
    MenuButtonCommands,
    BotCommand,
    BotCommandScopeChat
)

app = Client("my_bot")

from handlers._start import _start
from handlers._about import _about
from handlers._reset import _reset
from respond import respond


@app.on_message(filters.command("start") & filters.private)
async def start_handler(app, message):
    await _start(app, message)

@app.on_message(filters.command("about") & filters.private)
async def about_handler(app, message):
    await _about(app, message)

@app.on_message(filters.command("reset") & filters.private)
async def reset_handler(app, message):
    await _reset(app, message)

@app.on_message(filters.command("create_wallet") & filters.private)
async def create_wallet_handler(app, message):
    await _create_wallet(app, message)

@app.on_message(filters.text & filters.private)
async def respond_handler(app,message):
    await respond(message)

app.run()