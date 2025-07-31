import random
from pyrogram import Client, filters

# --- Tumhare bot credentials ---
API_ID = 24566510
API_HASH = "c2ee7f7c08ba307cf2e1eeca7f5d3381"
BOT_TOKEN = "8273816619:AAGKKfZSiOkF2TaDMATmhQ8lppB_AxwmrKg"

app = Client(
    "escrow_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("add", prefixes="/"))
async def add_amount(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: /add <amount>")

    try:
        amount = float(message.command[1])
        user1 = message.from_user.mention  # Auto username of sender

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
            f"Continue the Deal {user1}\n\n"
            f"Escrowed By : **Rebel Bot**"
        )

        await message.reply_text(msg)
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

print("✅ Auto-Username Escrow Bot Started...")
app.run()
