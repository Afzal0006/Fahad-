import re
import random
import json
from pyrogram import Client, filters
from pyrogram.types import Message

# Fill your API credentials and your userbot string session here
API_ID = 1234567  # your api_id
API_HASH = "your_api_hash"
STRING_SESSION = "your_string_session_here"

DATA_FILE = "data.json"
LOG_CHANNEL_ID = -1002330347621  # your log channel id

# Load/save data functions same as your bot
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

def init_group(chat_id: str):
    if chat_id not in data["groups"]:
        data["groups"][chat_id] = {
            "deals": {},
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

    data["global"]["total_deals"] += 1
    data["global"]["total_volume"] += amount
    data["global"]["total_fee"] += fee
    data["global"]["escrowers"][escrower] = data["global"]["escrowers"].get(escrower, 0) + amount

    save_data()

# Helper: Check if user is admin — for userbot, treat yourself as admin always
async def is_admin(m: Message):
    # Since you are the user running the userbot, we treat you as admin
    return True

# Commands handlers

async def start_handler(client: Client, message: Message):
    msg = (
        "✨ <b>Welcome to Demo Escrower Userbot!</b> ✨\n\n"
        "🤖 <b>I am here to manage escrow deals securely.</b>\n"
        "💡 Use me to hold payments safely until trades are complete.\n\n"
        "📋 <b>My Commands:</b>\n"
        "• <b>/add</b> – Add a new deal (Reply to DEAL INFO form)\n"
        "• <b>/complete</b> – Complete a deal (Auto release amount)\n"
        "• <b>/stats</b> – Show this group’s stats\n"
        "• <b>/gstats</b> – Show global stats\n\n"
        "🛡️ <i>Secure your trades with confidence!</i>"
    )
    await message.reply_text(msg, parse_mode="html")

async def add_deal_handler(client: Client, message: Message):
    if not await is_admin(message):
        return

    try:
        await message.delete()
    except:
        pass

    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to the DEAL INFO form message!")
        return

    original_text = message.reply_to_message.text or ""
    chat_id = str(message.chat.id)
    reply_id = str(message.reply_to_message.message_id)
    init_group(chat_id)

    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    amount_match = re.search(r"DEAL AMOUNT\s*:\s*₹?\s*([\d.]+)", original_text, re.IGNORECASE)

    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"
    
    if not amount_match:
        await message.reply_text("❌ Amount not found in the form!")
        return
    
    amount = float(amount_match.group(1))

    group_data = data["groups"][chat_id]
    if reply_id not in group_data["deals"]:
        trade_id = f"TID{random.randint(100000, 999999)}"
        fee = round(amount * 0.02, 2)
        release_amount = round(amount - fee, 2)
        group_data["deals"][reply_id] = {
            "trade_id": trade_id,
            "release_amount": release_amount,
            "completed": False
        }
    else:
        trade_id = group_data["deals"][reply_id]["trade_id"]
        release_amount = group_data["deals"][reply_id]["release_amount"]
        fee = round(amount - release_amount, 2)

    escrower = (
        f"@{message.from_user.username}" 
        if message.from_user.username 
        else message.from_user.first_name
    )

    update_escrower_stats(chat_id, escrower, amount, fee)

    msg = (
        "✅ <b>Amount Received!</b>\n"
        "────────────────\n"
        f"👤 <b>Buyer</b>  : {buyer}\n"
        f"👤 <b>Seller</b> : {seller}\n"
        f"💰 <b>Amount</b> : ₹{amount}\n"
        f"💸 <b>Release</b>: ₹{release_amount}\n"
        f"⚖️ <b>Fee</b>    : ₹{fee}\n"
        f"🆔 <b>Trade ID</b>: #{trade_id}\n"
        "────────────────\n"
        f"🛡️ <b>Escrowed by</b> {escrower}"
    )

    await client.send_message(
        chat_id, 
        msg, 
        reply_to_message_id=message.reply_to_message.message_id,
        parse_mode="html"
    )
    save_data()

async def complete_deal_handler(client: Client, message: Message):
    if not await is_admin(message):
        return

    try:
        await message.delete()
    except:
        pass

    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to the DEAL INFO form message!")
        return

    chat_id = str(message.chat.id)
    reply_id = str(message.reply_to_message.message_id)
    init_group(chat_id)

    group_data = data["groups"][chat_id]
    deal_info = group_data["deals"].get(reply_id)

    if not deal_info:
        await message.reply_text("❌ This deal was never added with /add!")
        return

    if deal_info["completed"]:
        await message.reply_text("❌ This deal is already completed!")
        return

    deal_info["completed"] = True
    save_data()

    original_text = message.reply_to_message.text or ""
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    trade_id = deal_info["trade_id"]
    release_amount = deal_info["release_amount"]
    escrower = (
        f"@{message.from_user.username}" 
        if message.from_user.username 
        else message.from_user.first_name
    )

    # Group message
    msg = (
        "✅ <b>Deal Completed!</b>\n"
        "────────────────\n"
        f"👤 <b>Buyer</b>   : {buyer}\n"
        f"👤 <b>Seller</b>  : {seller}\n"
        f"💸 <b>Released</b>: ₹{release_amount}\n"
        f"🆔 <b>Trade ID</b>: #{trade_id}\n"
        "────────────────\n"
        f"🛡️ <b>Escrowed by</b> {escrower}"
    )
    await client.send_message(
        chat_id, 
        msg, 
        reply_to_message_id=message.reply_to_message.message_id,
        parse_mode="html"
    )

    # Log channel
    log_msg = (
        "📜 <b>Deal Completed (Log)</b>\n"
        "────────────────\n"
        f"👤 <b>Buyer</b>   : {buyer}\n"
        f"👤 <b>Seller</b>  : {seller}\n"
        f"💸 <b>Released</b>: ₹{release_amount}\n"
        f"🆔 <b>Trade ID</b>: #{trade_id}\n"
        f"🛡️ <b>Escrowed by</b> {escrower}\n\n"
        f"📌 <b>Group</b>: {message.chat.title} ({message.chat.id})"
    )
    await client.send_message(LOG_CHANNEL_ID, log_msg, parse_mode="html")

async def stats_handler(client: Client, message: Message):
    chat_id = str(message.chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    escrowers_text = "\n".join([f"{name} = ₹{amt}" for name, amt in g["escrowers"].items()]) or "No deals yet"

    msg = (
        f"📊 Escrow Bot Stats\n\n"
        f"{escrowers_text}\n\n"
        f"🔹 Total Deals: {g['total_deals']}\n"
        f"💰 Total Volume: ₹{g['total_volume']}\n"
        f"💸 Total Fee Collected: ₹{g['total_fee']}\n"
    )
    await message.reply_text(msg)

async def gstats_handler(client: Client, message: Message):
    # Userbot owner only (you) can run this
    if not await is_admin(message):
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
    await message.reply_text(msg)

# Run the userbot client
app = Client(session_name=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

# Register command handlers as message handlers with filters
app.add_handler(filters.command("start") & filters.me, start_handler)
app.add_handler(filters.command("add") & filters.me, add_deal_handler)
app.add_handler(filters.command("complete") & filters.me, complete_deal_handler)
app.add_handler(filters.command("stats") & filters.me, stats_handler)
app.add_handler(filters.command("gstats") & filters.me, gstats_handler)

print("Userbot started... ✅")
app.run()
