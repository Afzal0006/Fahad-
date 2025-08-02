import re
import random
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8350094964:AAEBEZh1imgSPFA6Oc3-wdDGNyKV4Ozc_yg"
DATA_FILE = "data.json"
LOG_CHANNEL_ID = -1002330347621

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"groups": {}, "global": {"total_deals": 0, "total_volume": 0, "total_fee": 0.0, "escrowers": {}}}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

async def is_admin(update: Update) -> bool:
    try:
        member = await update.effective_chat.get_member(update.effective_user.id)
        return member.status in ["administrator", "creator"]
    except:
        return False

def init_group(chat_id: str):
    if chat_id not in data["groups"]:
        data["groups"][chat_id] = {
            "deals": {},
            "total_deals": 0,
            "total_volume": 0,
            "total_fee": 0.0,
            "escrowers": {},
            "buyers": {},
            "sellers": {}
        }

def update_escrower_stats(group_id: str, escrower: str, amount: float, fee: float):
    g = data["groups"][group_id]
    g["total_deals"] += 1
    g["total_volume"] += amount
    g["total_fee"] += fee
    g["escrowers"][escrower] = g["escrowers"].get(escrower, 0) + amount

    data["global"]["total_deals"] += 1
    data["global"]["total_volume"] += amount
    data["global"]["total_fee"] += fee
    data["global"]["escrowers"][escrower] = data["global"]["escrowers"].get(escrower, 0) + amount

    save_data()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "✨ <b>Welcome to Demo Escrower Bot!</b> ✨\n\n"
        "🤖 I manage escrow deals securely.\n"
        "💡 Hold payments safely until trades complete.\n\n"
        "📋 Commands:\n"
        "/add – Add new deal\n"
        "/complete – Complete a deal\n"
        "/refund – Refund a deal\n"
        "/pending – Show pending deals\n"
        "/history – Show recent deals\n"
        "/leaderboard – Top buyers & sellers\n"
        "/stats – Group stats\n"
        "/gstats – Global stats (Admin)\n\n"
        "🛡️ Secure your trades with confidence!"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

async def add_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return
    try:
        await update.message.delete()
    except:
        pass

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to DEAL INFO message!")
        return

    original_text = update.message.reply_to_message.text
    chat_id = str(update.effective_chat.id)
    reply_id = str(update.message.reply_to_message.message_id)
    init_group(chat_id)

    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    amount_match = re.search(r"DEAL AMOUNT\s*:\s*₹?\s*([\d.]+)", original_text, re.IGNORECASE)

    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"
    
    if not amount_match:
        await update.message.reply_text("❌ Amount not found!")
        return
    
    amount = float(amount_match.group(1))
    group_data = data["groups"][chat_id]

    if reply_id not in group_data["deals"]:
        trade_id = f"TID{random.randint(100000, 999999)}"
        fee = round(amount * 0.02, 2)
        release_amount = round(amount - fee, 2)
        group_data["deals"][reply_id] = {
            "trade_id": trade_id,
            "amount": amount,
            "release_amount": release_amount,
            "fee": fee,
            "status": "pending"
        }
    else:
        deal = group_data["deals"][reply_id]
        trade_id = deal["trade_id"]
        release_amount = deal["release_amount"]
        fee = deal["fee"]

    escrower = (
        f"@{update.effective_user.username}" 
        if update.effective_user.username 
        else update.effective_user.full_name
    )

    update_escrower_stats(chat_id, escrower, amount, fee)
    group_data["buyers"][buyer] = group_data["buyers"].get(buyer, 0) + amount
    group_data["sellers"][seller] = group_data["sellers"].get(seller, 0) + amount

    msg = (
        "✅ <b>Amount Received!</b>\n"
        f"👤 Buyer : {buyer}\n"
        f"👤 Seller: {seller}\n"
        f"💰 Amount: ₹{amount}\n"
        f"💸 Release: ₹{release_amount}\n"
        f"⚖️ Fee: ₹{fee}\n"
        f"🆔 Trade ID: #{trade_id}\n"
        f"🛡️ Escrowed by {escrower}"
    )
    await update.effective_chat.send_message(
        msg, 
        reply_to_message_id=update.message.reply_to_message.message_id,
        parse_mode="HTML"
    )
    save_data()

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    top_buyers = sorted(g["buyers"].items(), key=lambda x: x[1], reverse=True)[:5]
    top_sellers = sorted(g["sellers"].items(), key=lambda x: x[1], reverse=True)[:5]

    buyers_text = "\n".join([f"{i+1}. {name} – ₹{amt}" for i, (name, amt) in enumerate(top_buyers)]) or "No buyers yet"
    sellers_text = "\n".join([f"{i+1}. {name} – ₹{amt}" for i, (name, amt) in enumerate(top_sellers)]) or "No sellers yet"

    msg = (
        "🏆 <b>Top Buyers & Sellers</b>\n\n"
        f"👥 <b>Top Buyers</b>\n{buyers_text}\n\n"
        f"💼 <b>Top Sellers</b>\n{sellers_text}"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_deal))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    # Add other commands same pattern: complete, refund, pending, history, stats, gstats

    print("Bot started... ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
