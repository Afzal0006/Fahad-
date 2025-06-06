import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION_STRING")

bot = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    await event.reply("Pong! ✅")

print("⚡ Userbot Started...")
bot.start()
bot.run_until_disconnected()
