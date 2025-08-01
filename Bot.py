import re
import random
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token
DATA_FILE = "data.json"

# ================== LOAD / SAVE DATA ==================
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "groups": {},
            "global": {"total_deals": 0, "total_volume": 0, "total_fee": 0.0},
            "last_trade_id": 100000
        }

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

def init_group(chat_id: str, chat_name: str = ""):
    if chat_id not in data["groups"]:
        data["groups"][chat_id] = {
            "name": chat_name or f"Group-{chat_id}",
            "trade_ids": {},
            "deal_amounts": {},
            "total_deals": 0,
            "total_volume": 0,
            "total_fee": 0.0,
            "escrowers": {}
        }

def update_escrower_stats(group_id: str, escrower: str, amount: float, fee: float):
    g = data["groups"][group_id]
    g["total_deals"] += 1
    g["total_volume"] += amount
    g["total_fee"] += fee
    g["escrowers"][escrower] = g["escrowers"].get(escrower, 0) + amount

    # Global stats
    data["global"]["total_deals"] += 1
    data["global"]["total_volume"] += amount
    data["global"]["total_fee"] += fee
    save_data()

def generate_trade_id():
    data["last_trade_id"] += 1
    save_data()
    return f"TID{data['last_trade_id']}"

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

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to the DEAL INFO form message!")
        return

    original_text = update.message.reply_to_message.text
    chat_id = str(update.effective_chat.id)
    chat_name = update.effective_chat.title or "Private Chat"
    reply_id = str(update.message.reply_to_message.message_id)

    init_group(chat_id, chat_name)

    # ✅ Format-based Amount Detection
    amount = None
    if len(context.args) >= 1:
        try:
            amount = float(context.args[0])
        except:
            await update.message.reply_text("❌ Invalid amount!")
            return
    else:
        for line in original_text.splitlines():
            if line.strip().upper().startswith("DEAL AMOUNT"):
                amount_str = re.sub(r"[^\d.]", "", line)
                if amount_str:
                    amount = float(amount_str)
                break

    if amount is None:
        await update.message.reply_text("❌ Could not detect amount from form. Please provide manually.")
        return

    # Extract info
    deal_info_match = re.search(r"DEAL INFO\s*:\s*(.+)", original_text, re.IGNORECASE)
    deal_info = deal_info_match.group(1) if deal_info_match else ""
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    # Generate Trade ID if new
    if reply_id not in data["groups"][chat_id]["trade_ids"]:
        trade_id = generate_trade_id()
        data["groups"][chat_id]["trade_ids"][reply_id] = trade_id
        data["groups"][chat_id]["deal_amounts"][reply_id] = amount
    else:
        trade_id = data["groups"][chat_id]["trade_ids"][reply_id]

    # Fee calculation
    fee = round(amount * 0.02, 2)
    release_amount = round(amount - fee, 2)
    escrower = f"@{update.effective_user.username}" if update.effective_user.username else "Unknown"

    # Update stats
    update_escrower_stats(chat_id, escrower, amount, fee)

    # Final message
    msg = (
        f"💰 DEAL INFO : {deal_info}\n"
        f"BUYER : {buyer}\n"
        f"SELLER : {seller}\n"
        f"DEAL AMOUNT : ₹{amount}\n\n"
        f"💸 Release/Refund Amount: ₹{release_amount}\n"
        f"⚖️ Escrow Fee: ₹{fee}\n"
        f"🆔 Trade ID: #{trade_id}\n\n"
        f"🛡️ Escrowed By: {escrower}\n"
    )

    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)
    save_data()

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
    init_group(chat_id, update.effective_chat.title or "Private Chat")

    # Extract info
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    # Same Trade ID
    trade_id = data["groups"][chat_id]["trade_ids"].get(reply_id, generate_trade_id())
    escrower = f"@{update.effective_user.username}" if update.effective_user.username else "Unknown"

    msg = (
        f"✅ Deal Completed\n"
        f"🆔 Trade ID: #{trade_id}\n"
        f"ℹ️ Total Released: ₹{amount}\n\n"
        f"Buyer : {buyer}\n"
        f"Seller : {seller}\n\n"
        f"🛡️ Escrowed By: {escrower}\n"
    )

    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

# ================== /stats Command ==================
async def group_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    chat_name = update.effective_chat.title or "Private Chat"
    init_group(chat_id, chat_name)
    g = data["groups"][chat_id]

    escrowers_text = "\n".join([f"{name} = ₹{amt}" for name, amt in g["escrowers"].items()]) or "No deals yet"

    msg = (
        f"📊 Escrow Bot Stats\n{chat_name}\n\n"
        f"{escrowers_text}\n\n"
        f"🔹 Total Deals: {g['total_deals']}\n"
        f"💰 Total Volume: ₹{g['total_volume']}\n"
        f"💸 Total Fee Collected: ₹{g['total_fee']}\n"
    )
    await update.message.reply_text(msg)

# ================== /gstats Command ==================
async def global_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("❌ Only group admins can use this command.")
        return

    global_summary = data["global"]
    msg_lines = ["🌍 Global Escrow Stats\n"]

    for gid, g in data["groups"].items():
        if g["total_deals"] == 0:
            continue
        msg_lines.append(f"Group: {g['name']}")
        for name, amt in g["escrowers"].items():
            msg_lines.append(f"{name} = ₹{amt}")
        msg_lines.append("")  # blank line between groups

    msg_lines.append(f"🔹 Total Deals: {global_summary['total_deals']}")
    msg_lines.append(f"💰 Total Volume: ₹{global_summary['total_volume']}")
    msg_lines.append(f"💸 Total Fee Collected: ₹{global_summary['total_fee']}")

    await update.message.reply_text("\n".join(msg_lines))

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
