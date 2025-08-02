import re
import random
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"
DATA_FILE = "data.json"
LOG_CHANNEL_ID = -1002330347621  # apna log channel id

# ----------------- Data Handling -----------------
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

# ----------------- Utils -----------------
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
            "sellers": {},
            "history": []
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

# ----------------- Commands -----------------
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
            "buyer": buyer,
            "seller": seller,
            "amount": amount,
            "release_amount": release_amount,
            "fee": fee,
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }
    else:
        trade_id = group_data["deals"][reply_id]["trade_id"]

    escrower = (
        f"@{update.effective_user.username}" 
        if update.effective_user.username 
        else update.effective_user.full_name
    )

    update_escrower_stats(chat_id, escrower, amount, round(amount*0.02,2))
    group_data["buyers"][buyer] = group_data["buyers"].get(buyer, 0) + amount
    group_data["sellers"][seller] = group_data["sellers"].get(seller, 0) + amount

    msg = (
        "✅ <b>Amount Received!</b>\n"
        f"👤 Buyer : {buyer}\n"
        f"👤 Seller: {seller}\n"
        f"💰 Amount: ₹{amount}\n"
        f"💸 Release: ₹{amount - amount*0.02:.2f}\n"
        f"⚖️ Fee: ₹{amount*0.02:.2f}\n"
        f"🆔 Trade ID: #{trade_id}\n"
        f"🛡️ Escrowed by {escrower}"
    )
    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id, parse_mode="HTML")
    save_data()

async def complete_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to pending deal message!")
        return

    chat_id = str(update.effective_chat.id)
    reply_id = str(update.message.reply_to_message.message_id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    if reply_id not in g["deals"] or g["deals"][reply_id]["status"] != "pending":
        await update.message.reply_text("❌ No pending deal found for this message!")
        return

    deal = g["deals"][reply_id]
    deal["status"] = "completed"
    g["history"].append(deal)
    save_data()

    msg = (
        "🎉 <b>Deal Completed!</b>\n"
        f"👤 Buyer : {deal['buyer']}\n"
        f"👤 Seller: {deal['seller']}\n"
        f"💰 Amount: ₹{deal['amount']}\n"
        f"💸 Released: ₹{deal['release_amount']}\n"
        f"⚖️ Fee: ₹{deal['fee']}\n"
        f"🆔 Trade ID: #{deal['trade_id']}"
    )
    await update.effective_chat.send_message(msg, parse_mode="HTML")
    await context.bot.send_message(LOG_CHANNEL_ID, f"✅ Deal #{deal['trade_id']} Completed in Group {chat_id}", parse_mode="HTML")

async def refund_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to pending deal message to refund!")
        return

    chat_id = str(update.effective_chat.id)
    reply_id = str(update.message.reply_to_message.message_id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    if reply_id not in g["deals"] or g["deals"][reply_id]["status"] != "pending":
        await update.message.reply_text("❌ No pending deal found for this message!")
        return

    deal = g["deals"][reply_id]
    deal["status"] = "refunded"
    g["history"].append(deal)
    save_data()

    msg = (
        "💸 <b>Deal Refunded!</b>\n"
        f"👤 Buyer : {deal['buyer']}\n"
        f"👤 Seller: {deal['seller']}\n"
        f"💰 Amount: ₹{deal['amount']}\n"
        f"🆔 Trade ID: #{deal['trade_id']}"
    )
    await update.effective_chat.send_message(msg, parse_mode="HTML")
    await context.bot.send_message(LOG_CHANNEL_ID, f"⚠️ Deal #{deal['trade_id']} Refunded in Group {chat_id}", parse_mode="HTML")

async def pending_deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    pending_list = [d for d in g["deals"].values() if d["status"] == "pending"]
    if not pending_list:
        await update.message.reply_text("✅ No pending deals!")
        return

    msg = "⏳ <b>Pending Deals</b>\n\n"
    for d in pending_list:
        msg += f"🆔 #{d['trade_id']} | Buyer: {d['buyer']} | Amount: ₹{d['amount']}\n"
    await update.message.reply_text(msg, parse_mode="HTML")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    if not g["history"]:
        await update.message.reply_text("ℹ️ No past deals yet.")
        return

    last_deals = g["history"][-5:]
    msg = "📜 <b>Recent Deals</b>\n\n"
    for d in last_deals:
        msg += f"#{d['trade_id']} | {d['status'].capitalize()} | ₹{d['amount']}\n"
    await update.message.reply_text(msg, parse_mode="HTML")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    msg = (
        "📊 <b>Group Stats</b>\n\n"
        f"Total Deals: {g['total_deals']}\n"
        f"Total Volume: ₹{g['total_volume']}\n"
        f"Total Fee: ₹{g['total_fee']}"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

async def gstats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    g = data["global"]
    msg = (
        "🌎 <b>Global Stats</b>\n\n"
        f"Total Deals: {g['total_deals']}\n"
        f"Total Volume: ₹{g['total_volume']}\n"
        f"Total Fee: ₹{g['total_fee']}"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

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

# ----------------- Main -----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_deal))
    app.add_handler(CommandHandler("complete", complete_deal))
    app.add_handler(CommandHandler("refund", refund_deal))
    app.add_handler(CommandHandler("pending", pending_deals))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("gstats", gstats))
    app.add_handler(CommandHandler("leaderboard", leaderboard))

    print("Bot started... ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
