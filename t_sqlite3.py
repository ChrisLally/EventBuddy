#%%
import sqlite3,os,time,json

bot_db_name = "eventbuddy"

def createTable():
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    bot_db_c.execute(
    f'''CREATE TABLE IF NOT EXISTS {bot_db_name} (
    user_id TEXT PRIMARY KEY,
    transcript TEXT,
    sui_address TEXT,
    sui_privatekey TEXT,
    stellar_address TEXT,
    stellar_privatekey
    )'''
    )


def setTranscript(user_id, new_transcript):
    if type(new_transcript) is list:
        new_transcript = json.dumps(new_transcript)
    else:
        print("NEW TRANSCRIPT TYPE",type(new_transcript))
        
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    bot_db_c.execute(f"""
        INSERT OR REPLACE INTO {bot_db_name} (user_id, transcript)
        VALUES (?, ?)
    """, (user_id, new_transcript))
    bot_db_conn.commit()

def setSuiWallet(user_id, address,privatekey):
    if type(new_transcript) is list:
        new_transcript = json.dumps(new_transcript)
    else:
        print("NEW TRANSCRIPT TYPE",type(new_transcript))
        
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    bot_db_c.execute(f"""
        INSERT OR REPLACE INTO {bot_db_name} (user_id,sui_address, sui_privatekey)
        VALUES (?, ?)
    """, (user_id,address, privatekey))
    bot_db_conn.commit()

def setStellarPrivateKey(user_id, address,privatekey):
    if type(new_transcript) is list:
        new_transcript = json.dumps(new_transcript)
    else:
        print("NEW TRANSCRIPT TYPE",type(new_transcript))
        
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    bot_db_c.execute(f"""
        INSERT OR REPLACE INTO {bot_db_name} (user_id, stellar_address,stellar_privatekey)
        VALUES (?, ?)
    """, (user_id,address, privatekey))
    bot_db_conn.commit()

def resetChat(user_id):
    print('resetting chat',user_id)

    setTranscript(user_id,None)

def getTranscript(user_id):
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    doc = bot_db_c.execute(f"SELECT * FROM {bot_db_name} WHERE user_id=?",(user_id,)).fetchone()
    if doc is None:
        print('no doc, returning None',user_id)
        return None
        
    #print('full doc',doc)
    #print('doc1',doc[1])
    if doc[1] is None:
        print('no transcript, returning None',user_id)
        return None
    else:
        return json.loads(doc[1])
    
def getSuiWallet(user_id):
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    doc = bot_db_c.execute(f"SELECT * FROM {bot_db_name} WHERE user_id=?",(user_id,)).fetchone()
    if doc is None:
        print('no doc, returning None',user_id)
        return None
        
    #print('full doc',doc)
    #print('doc1',doc[1])
    if doc[2] is None:
        print('no transcript, returning None',user_id)
        return None
    else:
        return json.loads(doc[2])

def getStellarWallet(user_id):
    bot_db_conn = sqlite3.connect(f'bot/database/{bot_db_name}_db.sqlite')
    bot_db_c = bot_db_conn.cursor()
    doc = bot_db_c.execute(f"SELECT * FROM {bot_db_name} WHERE user_id=?",(user_id,)).fetchone()
    if doc is None:
        print('no doc, returning None',user_id)
        return None
        
    #print('full doc',doc)
    #print('doc1',doc[1])
    if doc[3] is None:
        print('no transcript, returning None',user_id)
        return None
    else:
        return json.loads(doc[3])
#%%
#createTable()
# %%
