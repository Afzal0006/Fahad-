
from telethon import TelegramClient, events
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

client = TelegramClient("userbot", api_id, api_hash)

@client.on(events.NewMessage(pattern="(?i).hi"))
async def handler(event):
    await event.reply("Hello! I'm your Userbot 😎")

client.start()
print("Userbot Started...")
client.run_until_disconnected()
