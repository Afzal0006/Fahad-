from telethon import TelegramClient, events

API_ID = 123456
API_HASH = "your_api_hash"
SESSION = "userbot_session"

client = TelegramClient(SESSION, API_ID, API_HASH)

@client.on(events.NewMessage(pattern="^/ping$"))
async def ping(event):
    if event.is_group:
        admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=client.iter_admins)]
        if event.sender_id in admins:
            await event.reply("Pong! ✅")

client.start()
client.run_until_disconnected()
