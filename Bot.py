import os
import random
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION_NAME", "userbot")

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
