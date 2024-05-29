import ai_prediction, t_sqlite3, json

async def respond(message):
    await message.reply_text("got your message...")
    
    message_history=t_sqlite3.getTranscript(message.chat.id)
    if message_history is None:
        print("NO MESSAGE HISTORY?? respond.py")
        from handlers import _start
        message_history=[{"is_user":True,"message":"/start"},{"is_user":False,"message": _start.start_message}]
        print("transcript_old is None, but got from _start", message_history)
        
    response="got your message..."
    #response=ai_prediction.generateResponse(message.text,message_history)
    message_history.append({
        "is_user":True,
        "message":message.text
    })
    message_history.append({
        "is_user":False,
        "message":response
    })

    t_sqlite3.setTranscript(message.chat.id,json.dumps(message_history))

    print('got response_text, now replying...')
    await message.reply_text(response)
