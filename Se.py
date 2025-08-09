from pyrogram import Client, filters
from pymongo import MongoClient

# ---------- CONFIG ----------
API_ID = 20917743
API_HASH = "0e8bcef16b3bae4f852bf42775f04ace"
BOT_TOKEN = "8414351117:AAEDEkc1VblJ8NU8Umle1gby1KyY94Gd1x4"
OWNER_ID = 6998916494

# Tumhara MongoDB Atlas URI
MONGO_URI = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

DB_NAME = "myDatabase"
# ----------------------------

# Pyrogram Bot
app = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# MongoDB Client
mongo_client = MongoClient(MONGO_URI)

# Owner-only command
@app.on_message(filters.command("resetdb") & filters.user(OWNER_ID))
def reset_database(_, message):
    try:
        # Step 1: Database drop
        mongo_client.drop_database(DB_NAME)
        
        # Step 2: Default data insert
        db = mongo_client[DB_NAME]
        db.config.insert_one({
            "owner_id": OWNER_ID,
            "bot_name": "MyBot",
            "language": "hi",
            "version": "1.0"
        })
        db.users.insert_one({
            "_id": OWNER_ID,
            "username": message.from_user.username or "Owner",
            "is_admin": True
        })
        
        message.reply_text(f"✅ Database `{DB_NAME}` reset ho gaya aur default data insert ho gaya!")
    
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")

# Agar koi non-owner try kare
@app.on_message(filters.command("resetdb") & ~filters.user(OWNER_ID))
def not_owner(_, message):
    message.reply_text("🚫 Ye command sirf owner ke liye hai!")

app.run()
