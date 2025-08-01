import re, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

# Runtime stats (reset on restart)
stats = {}

trade_id_counter = 1

def get_escrower(update: Update):
    return f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name

async def is_admin(update: Update) -> bool:
    chat = update.effective_chat
    user = update.effective_user
    try:
        member = await chat.get_member(user.id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# -------- /add --------
async def add_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global trade_id_counter
    if not await is_admin(update):
        await update.message.reply_text(f"{get_escrower(update)} Baag bhosadiya k")
        return

    try: await update.message.delete()
    except: pass

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to Deal Info message!")
        return

    original_text = update.message.reply_to_message.text

    # Smart Amount Detection
    match = re.search(r"DEAL\s*AMOUNT\s*[:\-]?\s*₹?\s*([\d.,]+)", original_text, re.IGNORECASE)
    if not match:
        await update.message.reply_text("❌ Amount detect nahi hua!")
        return
    amount = float(match.group(1).replace(",", ""))

    # Fee & release
    fee = round(amount * 0.02, 2)
    release = round(amount - fee, 2)

    # Extract buyer/seller
    buyer = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer.group(1) if buyer else "Unknown"
    seller = seller.group(1) if seller else "Unknown"

    trade_id = f"TID{trade_id_counter}"
    trade_id_counter += 1

    chat_id = str(update.effective_chat.id)
    if chat_id not in stats: stats[chat_id] = {"escrowers": {}, "total_deals": 0, "total_volume": 0}
    g = stats[chat_id]
    g["total_deals"] += 1
    g["total_volume"] += amount
    escrower = get_escrower(update)
    g["escrowers"][escrower] = g["escrowers"].get(escrower, 0) + amount

    deal_info = re.search(r"DEAL INFO\s*:\s*(.+)", original_text, re.IGNORECASE)
    deal_info = deal_info.group(1) if deal_info else "Unknown"

    msg = (
        f"💰 DEAL INFO : {deal_info}\n"
        f"BUYER : {buyer}\nSELLER : {seller}\n"
        f"DEAL AMOUNT : ₹{amount}\n\n"
        f"💸 Release/Refund Amount: ₹{release}\n"
        f"⚖️ Escrow Fee: ₹{fee}\n"
        f"🆔 Trade ID: #{trade_id}\n\n"
        f"🛡️ Escrowed By: {escrower}"
    )
    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

# -------- /complete --------
async def complete_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text(f"{get_escrower(update)} Baag bhosadiya k")
        return
    try: await update.message.delete()
    except: pass

    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: /complete <amount>")
        return

    try:
        amount = float(context.args[0])
    except:
        await update.message.reply_text("❌ Invalid amount!")
        return

    fee = round(amount * 0.02, 2)
    release = round(amount - fee, 2)

    original_text = update.message.reply_to_message.text if update.message.reply_to_message else ""
    buyer = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer.group(1) if buyer else "Unknown"
    seller = seller.group(1) if seller else "Unknown"

    trade_id = re.search(r"TID\d+", original_text)
    trade_id = trade_id.group(0) if trade_id else "TID?"

    msg = (
        f"✅ Deal Completed\n"
        f"🆔 Trade ID: #{trade_id}\n"
        f"ℹ️ Total Released: ₹{release}\n\n"
        f"Buyer : {buyer}\nSeller : {seller}\n\n"
        f"🛡️ Escrowed By: {get_escrower(update)}"
    )
    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

# -------- /stats --------
async def group_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    g = stats.get(chat_id, {"escrowers": {}, "total_deals": 0, "total_volume": 0})
    escrowers_text = "\n".join([f"{name} = ₹{amt}" for name, amt in g["escrowers"].items()]) or "No deals yet"
    msg = (
        f"📊 Escrow Bot Stats\n{escrowers_text}\n\n"
        f"🔹 Total Deals: {g['total_deals']}\n"
        f"💰 Total Volume: ₹{g['total_volume']}"
    )
    await update.message.reply_text(msg)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("add", add_deal))
    app.add_handler(CommandHandler("complete", complete_deal))
    app.add_handler(CommandHandler("stats", group_stats))
    print("🤖 Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
