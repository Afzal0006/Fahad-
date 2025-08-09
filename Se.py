from pyrogram import Client, filters
from pymongo import MongoClient

# ---------- CONFIG ----------
API_ID = 123456      # Apna API ID
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
OWNER_ID = 123456789  # Tumhara Telegram user ID
MONGO_URI = "mongodb://localhost:27017/"  # MongoDB URI
DB_NAME = "myDatabase"  # Tumhara DB naam
# ----------------------------

# Pyrogram Bot
app = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# MongoDB Client
mongo_client = MongoClient(MONGO_URI)

# Owner-only command
@app.on_message(filters.command("resetdb") & filters.user(OWNER_ID))
def reset_database(_, message):
    try:
        mongo_client.drop_database(DB_NAME)
        message.reply_text(f"✅ Database `{DB_NAME}` reset ho gaya!")
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")

# Agar koi non-owner try kare
@app.on_message(filters.command("resetdb") & ~filters.user(OWNER_ID))
def not_owner(_, message):
    message.reply_text("🚫 Ye command sirf owner ke liye hai!")

app.run()
