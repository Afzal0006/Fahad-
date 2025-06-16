import asyncio
import pytz
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl import functions
from dotenv import load_dotenv
import os
import threading
import time
import logging
from flask import Flask

# 🔐 Load secrets from .env
load_dotenv()
api_id = 28327193
api_hash = '4aa7d6f0ae2f65fc8c80c69f03d00ae1'
session_string = os.getenv("BQGwPRkAPJdoIi9zcBTIc_CcMvRXbauaWBHK2OXg19mEqYNRaPnaZUg1H_SIOZV0WF8yebZjFTrqLq5qnMK_iF6GW2pq4188rqUhihE25xwCFVT-IMv-Z7z4YECYyrZGBEAYngipw6k-vL0gg-BlPOI68-GVStn-QNnTI8gKFEIisbHBVBv0raY69W7Lk_OVnkUmZSvPNu-J7y4dt65fI6-z3vPyGW97QR6_a366vTXMGkdp8CZJ8EYVD5-731xwT1TVgqHudyWsYd_SmpQyw6qB4ahWPsGgtMTudZTK_-vSPxDbWKKrT5SQ5_AukJaCeV0wHARxj1yl2XJNeh0Fz9HMrOWbWAAAAAHceB2jAA")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# ✅ Flask App for keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 I am alive and running on Render!"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=8085)
    except Exception as e:
        logging.error(f"Error in Flask server: {e}")

def keep_alive():
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

# ✅ BIO Time updater
async def update_bio():
    base_bio = "You’re not better or smarter… just lucky, right time right place."
    while True:
        try:
            india = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(india).strftime("%I:%M %p IST")
            full_bio = f"{base_bio} | 🕒 {current_time}"
            await client(functions.account.UpdateProfileRequest(about=full_bio))
            print(f"[✓] Bio updated: {full_bio}")
        except Exception as e:
            print(f"[✗] Error updating bio: {e}")
        await asyncio.sleep(60)

async def keep_online_safe():
    while True:
        try:
            me = await client.get_me()
            messages = await client.get_messages("me", limit=1)
            if messages:
                await client.send_read_acknowledge("me", max_id=messages[0].id)
                print("[✓] Sent read receipt to keep session active")
        except Exception as e:
            print(f"[✗] Error in keep_online_safe: {e}")
        await asyncio.sleep(30)

# ✅ Toggle flag
message_edit_enabled = True  # default ON

# ✅ Command Handler: .on / .off
@client.on(events.NewMessage(outgoing=True, pattern=r"\.(on|off)"))
async def toggle_edit(event):
    global message_edit_enabled
    cmd = event.raw_text.lower().strip()
    if cmd == ".off":
        message_edit_enabled = False
        await event.reply("🛑 Message edit (code block) OFF।")
        print("[⚙️] Message edit feature turned OFF")
    elif cmd == ".on":
        message_edit_enabled = True
        await event.reply("✅ Message edit (code block) ACTIVE NOW।")
        print("[⚙️] Message edit feature turned ON")

# ✅ Message Code Block Quoter
@client.on(events.NewMessage(outgoing=True))
async def code_block_quote(event):
    global message_edit_enabled
    try:
        msg = event.raw_text
        if not message_edit_enabled:
            return
        if msg.startswith("") or msg.startswith("/") or msg.startswith(">") or msg.startswith(".on") or msg.startswith(".off"):
            return
        await asyncio.sleep(0.5)
        await event.edit(f"{msg}")
        print(f"[✓] Quoted in code block: {msg}")
    except Exception as e:
        print(f"[✗] Error in message quote: {e}")

# ✅ Start Everything
async def main():
    keep_alive()  # 🟢 Start Flask thread
    await client.start()
    print("✅ Bot started")
    await asyncio.gather(
        update_bio(),
        keep_online_safe()
    )

client.loop.run_until_complete(main())
