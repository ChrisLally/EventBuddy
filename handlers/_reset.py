import t_sqlite3

async def _reset(app, message):
    t_sqlite3.resetChat(message.chat.id)
    await message.reply_text("Bot has been reset.") #TODO /start again?