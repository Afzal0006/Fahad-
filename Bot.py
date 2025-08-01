import re
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8358410115:AAF6mtD7Mw1YEn6LNWdEJr6toCubTOz3NLg"

# Runtime stats
total_deals = 0
total_volume = 0
total_fee = 0.0

# ✅ Check Admin
async def is_admin(update: Update) -> bool:
    chat = update.effective_chat
    user = update.effective_user
    try:
        member = await chat.get_member(user.id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# 🔹 /add Command
async def add_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_deals, total_volume, total_fee

    if not await is_admin(update):
        username = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
        await update.message.reply_text(f"{username} Baag bhosadiya k")
        return

    try:
        await update.message.delete()
    except:
        pass

    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: Reply to DEAL INFO message with /add <amount>")
        return

    try:
        amount = float(context.args[0])
    except:
        await update.message.reply_text("❌ Invalid amount!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to the DEAL INFO form message!")
        return

    original_text = update.message.reply_to_message.text

    # Extract buyer, seller and time
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    time_match = re.search(r"TIME TO COMPLETE DEAL\s*:\s*(.+)", original_text, re.IGNORECASE)

    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"
    deal_time = time_match.group(1) if time_match else "Not Specified"

    # Calculate fee
    fee = round(amount * 0.02, 2)
    release_amount = round(amount - fee, 2)
    trade_id = f"TID{random.randint(100000, 999999)}"
    escrower = f"@{update.effective_user.username}" if update.effective_user.username else "Unknown"

    # Update stats
    total_deals += 1
    total_volume += amount
    total_fee += fee

    # Final message
    msg = (
        f"💰 DEAL INFO :\n"
        f"BUYER : {buyer}\n"
        f"SELLER : {seller}\n"
        f"DEAL AMOUNT : ₹{amount}\n"
        f"TIME TO COMPLETE DEAL : {deal_time}\n\n"
        f"💸 Release/Refund Amount: ₹{release_amount}\n"
        f"⚖️ Escrow Fee: ₹{fee}\n"
        f"🆔 Trade ID: #{trade_id}\n\n"
        f"🛡️ Escrowed By: {escrower}\n"
    )

    await update.effective_chat.send_message(
        msg,
        reply_to_message_id=update.message.reply_to_message.message_id
    )

# 🔹 /complete Command
async def complete_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        username = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
        await update.message.reply_text(f"{username} Baag bhosadiya k")
        return

    try:
        await update.message.delete()
    except:
        pass

    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: Reply to DEAL INFO message with /complete <amount>")
        return

    try:
        amount = float(context.args[0])
    except:
        await update.message.reply_text("❌ Invalid amount!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to the DEAL INFO form message!")
        return

    original_text = update.message.reply_to_message.text

    # Extract buyer and seller
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)

    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    trade_id = f"TID{random.randint(100000, 999999)}"
    escrower = f"@{update.effective_user.username}" if update.effective_user.username else "Unknown"

    msg = (
        f"✅ Deal Completed\n"
        f"🆔 Trade ID: #{trade_id}\n"
        f"ℹ️ Total Released: ₹{amount}\n\n"
        f"Buyer : {buyer}\n"
        f"Seller : {seller}\n\n"
        f"🛡️ Escrowed By: {escrower}\n"
    )

    await update.effective_chat.send_message(
        msg,
        reply_to_message_id=update.message.reply_to_message.message_id
    )

# 🔹 Bot Start
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("add", add_deal))
    app.add_handler(CommandHandler("complete", complete_deal))
    print("Bot started... ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
