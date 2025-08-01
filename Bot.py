import json, re, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"groups": {}, "last_trade_id": 100000}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

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
            "escrowers": {}, "total_deals": 0, "total_volume": 0
        }

def generate_trade_id():
    data["last_trade_id"] += 1
    save_data()
    return f"TID{data['last_trade_id']}"

def get_escrower_name(update: Update):
    return f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name

async def add_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text(f"{get_escrower_name(update)} Baag bhosadiya k")
        return
    try: await update.message.delete()
    except: pass
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to Deal Info message!")
        return

    original_text = update.message.reply_to_message.text
    chat_id = str(update.effective_chat.id)
    init_group(chat_id)

    amount = None
    for line in original_text.splitlines():
        if "DEAL AMOUNT" in line.upper():
            amt = re.sub(r"[^\d.]", "", line)
            if amt: amount = float(amt); break
    if amount is None:
        await update.message.reply_text("❌ Amount detect nahi hua!")
        return

    fee = round(amount * 0.02, 2)
    release = round(amount - fee, 2)

    buyer = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer.group(1) if buyer else "Unknown"
    seller = seller.group(1) if seller else "Unknown"

    trade_id = generate_trade_id()
    g = data["groups"][chat_id]
    g["total_deals"] += 1
    g["total_volume"] += amount
    escrower = get_escrower_name(update)
    g["escrowers"][escrower] = g["escrowers"].get(escrower, 0) + amount
    save_data()

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

async def complete_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text(f"{get_escrower_name(update)} Baag bhosadiya k")
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
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to Deal Info message!")
        return

    fee = round(amount * 0.02, 2)
    release = round(amount - fee, 2)
    original_text = update.message.reply_to_message.text
    buyer = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer.group(1) if buyer else "Unknown"
    seller = seller.group(1) if seller else "Unknown"
    trade_id = re.search(r"TID\d+", original_text)
    trade_id = trade_id.group(0) if trade_id else generate_trade_id()

    msg = (
        f"✅ Deal Completed\n"
        f"🆔 Trade ID: #{trade_id}\n"
        f"ℹ️ Total Released: ₹{release}\n\n"
        f"Buyer : {buyer}\nSeller : {seller}\n\n"
        f"🛡️ Escrowed By: {get_escrower_name(update)}"
    )
    await update.effective_chat.send_message(msg, reply_to_message_id=update.message.reply_to_message.message_id)

async def group_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]
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
