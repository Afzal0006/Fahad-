from pyrogram import Client, filters
import random

BOT_TOKEN = "8358410115:AAF6mtD7Mw1YEn6LNWdEJr6toCubTOz3NLg"

app = Client("escrow_bot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("add"))
async def add_command(client, message):
    args = message.text.split()
    
    if len(args) < 2:
        await message.reply_text(
            "❌ Format:\n`/add <amount>`\n\nExample:\n`/add 100`"
        )
        return
    
    amount = float(args[1])
    fee = round(amount * 0.02, 2)  # 2% fee
    trade_id = f"#TID{random.randint(100000,999999)}"
    
    username = message.from_user.username
    escrowed_by = f"@{username}" if username else f"[User](tg://user?id={message.from_user.id})"
    
    msg = f"""
Recived Amount : {amount}
FEE (2%) : {fee}
Trade ID : {trade_id}

Escrowed By : {escrowed_by}
"""
    await message.reply_text(msg)

app.run()
