import os
import random
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load env
load_dotenv()

API_ID = int(os.getenv("24566510"))
API_HASH = os.getenv("c2ee7f7c08ba307cf2e1eeca7f5d3381")
SESSION = os.getenv("AQF22u4Aeprwn_km-PfgsUEu7VSBwvZiD9Gm5mbvMpFokYLWQTxWZ3ylb3nn6JfQnmpY9DQf2jY9oLgW2eGSpYyJ86vFtZe69t1hju4otfy-KA9vAZFVLqTielwM3zsu0tzYJ39rITGq1eLA0BKfOXH_F7XQrBTrod_tM9VDHDUeRBBElkxVT8sn0H62cC7qbaNUEEt05hw8CZesGMf5UCUTT_tttUqxMbBliml_A2va_iybYj0iV2zqu-vWXiY5uMVPgJrMRvfsbF4GzjWpNr9ALPA2nXYFLPgFLbomfCkOZME7vnLXYmiap7LMut8p3bGKw6cAt5Nch8jN92Y26aqXBgnE9QAAAAHSwzxWAA", "userbot")

client = TelegramClient(SESSION, API_ID, API_HASH)

# Start client
@client.on(events.NewMessage(pattern=r"^/add (\d+)$"))
async def add_amount(event):
    try:
        amount = int(event.pattern_match.group(1))  # Jo amount admin ne diya
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

        await event.reply(msg)
    except Exception as e:
        await event.reply(f"Error: {str(e)}")

print("Userbot started...")
client.start()
client.run_until_disconnected()
