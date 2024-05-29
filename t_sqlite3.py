#%%
import sqlite3,os,time,json

bot_db_name = "eventbuddy"

def createTable():
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    bot_db_c.execute(
    f'''CREATE TABLE IF NOT EXISTS {bot_db_name} (
    chat_id TEXT PRIMARY KEY,
    transcript TEXT
    )'''
    )


def setTranscript(chat_id, new_transcript):
    if type(new_transcript) is list:
        new_transcript = json.dumps(new_transcript)
    else:
        print("NEW TRANSCRIPT TYPE",type(new_transcript))
        
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    bot_db_c.execute(f"""
        INSERT OR REPLACE INTO {bot_db_name} (chat_id, transcript)
        VALUES (?, ?)
    """, (chat_id, new_transcript))
    bot_db_conn.commit()


def resetChat(chat_id):
    print('resetting chat',chat_id)

    setTranscript(chat_id,None)

def getTranscript(chat_id):
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    doc = bot_db_c.execute(f"SELECT * FROM {bot_db_name} WHERE chat_id=?",(chat_id,)).fetchone()
    if doc is None:
        print('no doc, returning None',chat_id)
        return None
        
    #print('full doc',doc)
    #print('doc1',doc[1])
    if doc[1] is None:
        print('no transcript, returning None',chat_id)
        return None
    else:
        return json.loads(doc[1])
#%%
#createTable()
# %%
