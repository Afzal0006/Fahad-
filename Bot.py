import re, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

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

    try:
        await update.message.delete()
    except:
        pass

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to Deal Info message!")
        return

    original_text = update.message.reply_to_message.text or ""

    # Extract fields
    deal_info = re.search(r"DEAL INFO\s*:\s*(.+)", original_text, re.IGNORECASE)
    buyer = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    amount = re.search(r"DEAL\s*AMOUNT\s*[:\-]?\s*₹?\s*([\d.,]+)", original_text, re.IGNORECASE)
    time_limit = re.search(r"TIME TO COMPLETE DEAL\s*:\s*(.+)", original_text, re.IGNORECASE)

    deal_info = deal_info.group(1).strip() if deal_info else "Not Specified"
    buyer = buyer.group(1) if buyer else "Unknown"
    seller = seller.group(1) if seller else "Unknown"
    amount = float(amount.group(1).replace(",", "")) if amount else 0
    time_limit = time_limit.group(1).strip() if time_limit else "Not Specified"

    fee = round(amount * 0.02, 2)
    release = round(amount - fee, 2)

    trade_id = f"TID{trade_id_counter}"
    trade_id_counter += 1

    msg = (
        f"💰 DEAL INFO : {deal_info}\n"
        f"BUYER : {buyer}\n"
        f"SELLER : {seller}\n"
        f"DEAL AMOUNT : ₹{amount}\n"
        f"TIME TO COMPLETE DEAL : {time_limit}\n\n"
        f"💸 Release/Refund Amount: ₹{release}\n"
        f"⚖️ Escrow Fee: ₹{fee}\n"
        f"🆔 Trade ID: #{trade_id}\n\n"
        f"🛡️ Escrowed By: {get_escrower(update)}"
    )
    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

# -------- /complete --------
async def complete_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text(f"{get_escrower(update)} Baag bhosadiya k")
        return

    try:
        await update.message.delete()
    except:
        pass

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to the original deal message to complete it!")
        return

    original_text = update.message.reply_to_message.text or ""

    # Extract original deal info
    deal_info = re.search(r"DEAL INFO\s*:\s*(.+)", original_text)
    buyer = re.search(r"BUYER\s*:\s*(@\w+)", original_text)
    seller = re.search(r"SELLER\s*:\s*(@\w+)", original_text)
    amount = re.search(r"DEAL AMOUNT\s*:\s*₹?([\d.,]+)", original_text)
    time_limit = re.search(r"TIME TO COMPLETE DEAL\s*:\s*(.+)", original_text)
    trade_id = re.search(r"TID\d+", original_text)

    deal_info = deal_info.group(1).strip() if deal_info else "Not Specified"
    buyer = buyer.group(1) if buyer else "Unknown"
    seller = seller.group(1) if seller else "Unknown"
    amount = float(amount.group(1).replace(",", "")) if amount else 0
    time_limit = time_limit.group(1).strip() if time_limit else "Not Specified"
    trade_id = trade_id.group(0) if trade_id else "TID?"

    fee = round(amount * 0.02, 2)
    release = round(amount - fee, 2)

    msg = (
        f"✅ DEAL COMPLETED\n"
        f"💰 DEAL INFO : {deal_info}\n"
        f"BUYER : {buyer}\n"
        f"SELLER : {seller}\n"
        f"DEAL AMOUNT : ₹{amount}\n"
        f"TIME TO COMPLETE DEAL : {time_limit}\n\n"
        f"💸 Total Released to Seller: ₹{release}\n"
        f"⚖️ Escrow Fee: ₹{fee}\n"
        f"🆔 Trade ID: #{trade_id}\n\n"
        f"🛡️ Escrowed By: {get_escrower(update)}"
    )
    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

# -------- Bot Runner --------
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("add", add_deal))
    app.add_handler(CommandHandler("complete", complete_deal))
    print("🤖 Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
