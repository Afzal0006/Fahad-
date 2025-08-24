from pyrogram import Client, filters
from pymongo import MongoClient

# ------------------ CONFIG ------------------
# Pyrogram / Telegram
STRING_SESSION = "BQFBrnYAl-pWnXbngB408FvSpoCaD7zojyTEPq9HUho4f_6juAcAzJ7TuF0v2TCZ0ahvEsEHjHhxWxyq9VbYwCh1mfUQvtHiy6WLaSor8F0g_jaz07f-W8_Gy6NQLiEJt_YXrhy4Py0L6MnTSxb4U_Xn4PWlQQ934BD-nh8BxyCgTV_DcQrvA8YwpWDGeKem1ZaAK8lQvtcCj5jmNs4WBHNSXchphObU_MxfZm_-lKCABX3CYY_I_CIyNMQH9WUIp2syavT-9iakCWa8WtMN-NFrxPc6LX14KxveI24ZmGeBj2_bwxWTDrzrJj4ppYiGZ6Xvo06tAlKkmFY4bihnqvTPgbopYAAAAAGxU39QAA"
API_ID = 21081718
API_HASH = "fec3c59a0f36beb71199dba4459eef86"

# MongoDB
MONGO_URI = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "filter_bot"
COLLECTION = "filters"

# Group & Fetch settings
GROUP_ID = -1002776165745      # Group ID jaha scan karna hai
MESSAGE_FETCH_LIMIT = 50       # Kitne recent messages scan karne hain
# -------------------------------------------

# ------------------ MONGODB SETUP ------------------
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION]

# ------------------ PYROGRAM CLIENT ------------------
app = Client(session_name=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

# ------------------ COMMAND HANDLER ------------------
@app.on_message(filters.command("Filter") & filters.chat(GROUP_ID))
async def filter_command(client, message):
    """
    User-triggered filter command
    Usage: /Filter <keyword>
    """
    # Check for keyword argument
    if len(message.command) < 2:
        await message.reply_text("Usage: /Filter <keyword>")
        return

    keyword = " ".join(message.command[1:]).lower()
    user_id = message.from_user.id

    # Fetch last checked message id for this user and keyword
    user_filter = collection.find_one({"user_id": user_id, "keyword": keyword})
    last_id = user_filter["last_checked_message_id"] if user_filter else 0

    # Fetch recent messages from group
    messages = await client.get_chat_history(GROUP_ID, limit=MESSAGE_FETCH_LIMIT)
    matched = []
    newest_id = last_id

    # Scan messages from oldest to newest
    for msg in reversed(messages):
        if msg.message and keyword in msg.message.lower() and msg.message_id > last_id:
            sender = msg.from_user.first_name if msg.from_user else "Unknown"
            matched.append(f"{sender}: {msg.message}")
            if msg.message_id > newest_id:
                newest_id = msg.message_id

    # Send results to user via DM
    if matched:
        response = "📌 Matched messages:\n\n" + "\n\n".join(matched)
        await client.send_message(user_id, response)
    else:
        await client.send_message(user_id, "No new messages found for this keyword.")

    # Update last checked message id in MongoDB
    collection.update_one(
        {"user_id": user_id, "keyword": keyword},
        {"$set": {"last_checked_message_id": newest_id}},
        upsert=True
    )

# ------------------ RUN THE BOT ------------------
print("✅ Userbot is running...")
app.run()
