from pyrogram import Client, filters

# --- Tumhare Pyrogram credentials ---
API_ID = 24566510  
API_HASH = "c2ee7f7c08ba307cf2e1eeca7f5d3381"
STRING_SESSION = "AQF22u4Aeprwn_km-PfgsUEu7VSBwvZiD9Gm5mbvMpFokYLWQTxWZ3ylb3nn6JfQnmpY9DQf2jY9oLgW2eGSpYyJ86vFtZe69t1hju4otfy-KA9vAZFVLqTielwM3zsu0tzYJ39rITGq1eLA0BKfOXH_F7XQrBTrod_tM9VDHDUeRBBElkxVT8sn0H62cC7qbaNUEEt05hw8CZesGMf5UCUTT_tttUqxMbBliml_A2va_iybYj0iV2zqu-vWXiY5uMVPgJrMRvfsbF4GzjWpNr9ALPA2nXYFLPgFLbomfCkOZME7vnLXYmiap7LMut8p3bGKw6cAt5Nch8jN92Y26aqXBgnE9QAAAAHSwzxWAA"

# Pyrogram userbot client
app = Client(
    name="userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# Command: /ping
@app.on_message(filters.me & filters.command("ping", prefixes="/"))
async def ping(client, message):
    await message.reply_text("✅ Userbot is Alive!")

# Command: /id
@app.on_message(filters.me & filters.command("id", prefixes="/"))
async def user_id(client, message):
    await message.reply_text(f"👤 Your User ID: `{message.from_user.id}`")

print("✅ Userbot started successfully...")
app.run()
