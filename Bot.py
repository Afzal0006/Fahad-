import asyncio
import pytz
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl import functions
from dotenv import load_dotenv
import os
import threading
import logging
from flask import Flask

# 🔐 Load environment variables from .env file
load_dotenv()

# ✅ Load API credentials safely
api_id = int(os.getenv("24566510"))
api_hash = os.getenv("c2ee7f7c08ba307cf2e1eeca7f5d3381")
session_string = os.getenv("SESSION_STRING")

# ✅ Create Telegram client
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# ✅ Enable logging
logging.basicConfig(level=logging.INFO)

# ✅ Flask server for uptime (Render, Replit, etc.)
app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 I am alive and running!"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=8085)
    except Exception as e:
        logging.error(f"Flask error: {e}")

def keep_alive():
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

# ✅ Bio updater
async def update_bio():
    base_bio = "You’re not better or smarter… just lucky, right time right place."
    while True:
        try:
            india = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(india).strftime("%I:%M %p IST")
            full_bio = f"{base_bio} | 🕒 {current_time}"
            await client(functions.account.UpdateProfileRequest(about=full_bio))
            logging.info(f"Bio updated: {full_bio}")
        except Exception as e:
            logging.error(f"Bio update error: {e}")
        await asyncio.sleep(60)

# ✅ Keep session active
async def keep_online_safe():
    while True:
        try:
            messages = await client.get_messages("me", limit=1)
            if messages:
                await client.send_read_acknowledge("me", max_id=messages[0].id)
                logging.info("Read receipt sent to self.")
        except Exception as e:
            logging.error(f"Keep-alive error: {e}")
        await asyncio.sleep(30)

# ✅ Toggle for message editing
message_edit_enabled = True

@client.on(events.NewMessage(outgoing=True, pattern=r"\.(on|off)"))
async def toggle_edit(event):
    global message_edit_enabled
    cmd = event.raw_text.lower().strip()
    if cmd == ".off":
        message_edit_enabled = False
        await event.reply("🛑 Message editing OFF")
        logging.info("Message edit OFF")
    elif cmd == ".on":
        message_edit_enabled = True
        await event.reply("✅ Message editing ON")
        logging.info("Message edit ON")

# ✅ Code block message editor
@client.on(events.NewMessage(outgoing=True))
async def code_block_quote(event):
    global message_edit_enabled
    msg = event.raw_text
    if not message_edit_enabled:
        return
    if msg.startswith("/") or msg.startswith(">") or msg.lower().startswith(".on") or msg.lower().startswith(".off"):
        return
    try:
        await asyncio.sleep(0.5)
        await event.edit(f"{msg}")
        logging.info(f"Message edited: {msg}")
    except Exception as e:
        logging.error(f"Message edit error: {e}")

# ✅ Main runner
async def main():
    keep_alive()
    await client.start()
    logging.info("✅ Bot is live and running.")
    await asyncio.gather(
        update_bio(),
        keep_online_safe()
    )

# ✅ Start everything
try:
    client.loop.run_until_complete(main())
except Exception as e:
    logging.error(f"❌ Bot startup failed: {e}")
