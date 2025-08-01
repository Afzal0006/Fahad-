import re
import random
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8358410115:AAF6mtD7Mw1YEn6LNWdEJr6toCubTOz3NLg"
DATA_FILE = "data.json"
GLOBAL_ADMIN = "@golgibody"  # Only this user can use /gstats

# ================== LOAD / SAVE DATA ==================
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"groups": {}, "global": {"total_deals": 0, "total_volume": 0, "total_fee": 0.0, "escrowers": {}}}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ================== HELPERS ==================
async def is_admin(update: Update) -> bool:
    chat = update.effective_chat
    user = update.effective_user
    try:
        member = await chat.get_member(user.id)
        return member.status in ["administrator", "creator"]
    except:
        return False

def init_group(chat_id: str):
    if chat_id not in data["groups"]:
        data["groups"][chat_id] = {
            "trade_ids": {},
            "total_deals": 0,
            "total_volume": 0,
            "total_fee": 0.0,
            "escrowers": {}
        }

def update_escrower_stats(group_id: str, escrower: str, amount: float, fee: float):
    # Group-wise stats
    g = data["groups"][group_id]
    g["total_deals"] += 1
    g["total_volume"] += amount
    g["total_fee"] += fee
    g["escrowers"][escrower] = g["escrowers"].get(escrower, 0) + amount

    # Global stats
    data["global"]["total_deals"] += 1
    data["global"]["total_volume"] += amount
    data["global"]["total_fee"] += fee
    data["global"]["escrowers"][escrower] = data["global"]["escrowers"].get(escrower, 0) + amount

    save_data()

# ================== /add Command ==================
async def add_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    chat_id = str(update.effective_chat.id)
    reply_id = str(update.message.reply_to_message.message_id)

    # Initialize group in data
    init_group(chat_id)

    # Extract buyer & seller
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    # Generate Trade ID if new
    if reply_id not in data["groups"][chat_id]["trade_ids"]:
        # 6-digit random Trade ID
        data["groups"][chat_id]["trade_ids"][reply_id] = f"TID{random.randint(100000, 999999)}"
        save_data()

    trade_id = data["groups"][chat_id]["trade_ids"][reply_id]

    # Fee calculation
    fee = round(amount * 0.02, 2)
    release_amount = round(amount - fee, 2)
    escrower = f"@{update.effective_user.username}" if update.effective_user.username else "Unknown"

    # Update stats
    update_escrower_stats(chat_id, escrower, amount, fee)

    # Final message
    msg = (
        f"💰 DEAL INFO :\n"
        f"BUYER : {buyer}\n"
        f"SELLER : {seller}\n"
        f"DEAL AMOUNT : ₹{amount}\n\n"
        f"💸 Release/Refund Amount: ₹{release_amount}\n"
        f"⚖️ Escrow Fee: ₹{fee}\n"
        f"🆔 Trade ID: #{trade_id}\n\n"
        f"🛡️ Escrowed By: {escrower}\n"
    )

    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

# ================== /complete Command ==================
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
    chat_id = str(update.effective_chat.id)
    reply_id = str(update.message.reply_to_message.message_id)
    init_group(chat_id)

    # Extract buyer & seller
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    # Get existing Trade ID (Do not generate new)
    trade_id = data["groups"][chat_id]["trade_ids"].get(reply_id, "Unknown")

    msg = (
        f"✅ Deal Completed\n"
        f"🆔 Trade ID: #{trade_id}\n"
        f"ℹ️ Total Released: ₹{amount}\n\n"
        f"Buyer : {buyer}\n"
        f"Seller : {seller}\n\n"
        f"🛡️ Escrowed By: @{update.effective_user.username if update.effective_user.username else 'Unknown'}\n"
    )

    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

# ================== /stats Command ==================
async def group_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    # Prepare escrower list
    escrowers_text = "\n".join([f"{name} = ₹{amt}" for name, amt in g["escrowers"].items()]) or "No deals yet"

    msg = (
        f"📊 Escrow Bot Stats\n\n"
        f"{escrowers_text}\n\n"
        f"🔹 Total Deals: {g['total_deals']}\n"
        f"💰 Total Volume: ₹{g['total_volume']}\n"
        f"💸 Total Fee Collected: ₹{g['total_fee']}\n"
    )
    await update.message.reply_text(msg)

# ================== /gstats Command ==================
async def global_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.first_name

    # Only @golgibody can use
    if username != GLOBAL_ADMIN:
        await update.message.reply_text("❌ You are not allowed to use this command.")
        return

    g = data["global"]
    escrowers_text = "\n".join([f"{name} = ₹{amt}" for name, amt in g["escrowers"].items()]) or "No deals yet"

    msg = (
        f"🌍 Global Escrow Stats\n\n"
        f"{escrowers_text}\n\n"
        f"🔹 Total Deals: {g['total_deals']}\n"
        f"💰 Total Volume: ₹{g['total_volume']}\n"
        f"💸 Total Fee Collected: ₹{g['total_fee']}\n"
    )
    await update.message.reply_text(msg)

# ================== Bot Start ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("add", add_deal))
    app.add_handler(CommandHandler("complete", complete_deal))
    app.add_handler(CommandHandler("stats", group_stats))
    app.add_handler(CommandHandler("gstats", global_stats))
    print("Bot started... ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
