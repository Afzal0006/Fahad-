import random
from pyrogram import Client, filters

# --- Apne Pyrogram credentials yaha daalo ---
API_ID = 24566510  # <- Apna API ID
API_HASH = "c2ee7f7c08ba307cf2e1eeca7f5d3381"  # <- Apna API HASH
STRING_SESSION = "AQF22u4Aeprwn_km-PfgsUEu7VSBwvZiD9Gm5mbvMpFokYLWQTxWZ3ylb3nn6JfQnmpY9DQf2jY9oLgW2eGSpYyJ86vFtZe69t1hju4otfy-KA9vAZFVLqTielwM3zsu0tzYJ39rITGq1eLA0BKfOXH_F7XQrBTrod_tM9VDHDUeRBBElkxVT8sn0H62cC7qbaNUEEt05hw8CZesGMf5UCUTT_tttUqxMbBliml_A2va_iybYj0iV2zqu-vWXiY5uMVPgJrMRvfsbF4GzjWpNr9ALPA2nXYFLPgFLbomfCkOZME7vnLXYmiap7LMut8p3bGKw6cAt5Nch8jN92Y26aqXBgnE9QAAAAHSwzxWAA"  # <- Apna Pyrogram string session

# Pyrogram client
app = Client(name="userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

@app.on_message(filters.me & filters.command("add", prefixes="/"))
async def add_amount(client, message):
    try:
        # Command check
        if len(message.command) < 2:
            return await message.reply_text("⚠️ Usage: `/add <amount>`")

        amount = int(message.command[1])
        fee_percent = 4

        fee = round(amount * fee_percent / 100, 2)
        release_amount = round(amount - fee, 2)
        trade_id = f"#TID{random.randint(100000,999999)}"

        msg = (
            "💰 **P.A.G.A.L INR Transactions**\n\n"
            f"💵 **Received Amount:** ₹{amount}\n"
            f"💸 **Release/Refund Amount:** ₹{release_amount}\n"
            f"💎 **Escrow Fee:** ₹{fee}\n"
            f"📌 **Trade ID:** {trade_id}\n\n"
            "✅ Continue the Deal..."
        )

        await message.reply_text(msg)
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

print("Pyrogram userbot started...")
app.run()
