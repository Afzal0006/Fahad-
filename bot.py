from telethon import TelegramClient, events, types, functions
import asyncio

API_ID = 28327193  # <-- Replace with your API ID
API_HASH = '4aa7d6f0ae2f65fc8c80c69f03d00ae1'  # <-- Replace with your API HASH
SESSION_NAME = 'BQGwPRkAPJdoIi9zcBTIc_CcMvRXbauaWBHK2OXg19mEqYNRaPnaZUg1H_SIOZV0WF8yebZjFTrqLq5qnMK_iF6GW2pq4188rqUhihE25xwCFVT-IMv-Z7z4YECYyrZGBEAYngipw6k-vL0gg-BlPOI68-GVStn-QNnTI8gKFEIisbHBVBv0raY69W7Lk_OVnkUmZSvPNu-J7y4dt65fI6-z3vPyGW97QR6_a366vTXMGkdp8CZJ8EYVD5-731xwT1TVgqHudyWsYd_SmpQyw6qB4ahWPsGgtMTudZTK_-vSPxDbWKKrT5SQ5_AukJaCeV0wHARxj1yl2XJNeh0Fz9HMrOWbWAAAAAHceB2jAA'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Basic Commands
@client.on(events.NewMessage(pattern=r'\.ping'))
async def ping(event):
    await event.reply("🏓 Pong!")

@client.on(events.NewMessage(pattern=r'\.alive'))
async def alive(event):
    await event.reply("✅ I'm Alive!")

@client.on(events.NewMessage(pattern=r'\.id'))
async def userid(event):
    sender = await event.get_sender()
    await event.reply(f"🆔 Your ID: `{sender.id}`")

@client.on(events.NewMessage(pattern=r'\.me'))
async def me(event):
    sender = await event.get_sender()
    name = sender.first_name or "Unknown"
    username = f"@{sender.username}" if sender.username else "No username"
    await event.reply(f"🙋‍♂️ Name: {name}\n🔹 Username: {username}\n🆔 ID: `{sender.id}`")

@client.on(events.NewMessage(pattern=r'\.info'))
async def info(event):
    replied = await event.get_reply_message()
    if not replied:
        await event.reply("❗ Kisi user ko reply karo jiska info chahiye.")
        return
    user = await replied.get_sender()
    msg = f"""📄 User Info:
• Name: {user.first_name}
• Username: @{user.username if user.username else 'None'}
• ID: `{user.id}`
• Bot: {user.bot}
• Restricted: {user.restricted}
"""
    await event.reply(msg)

# Admin Commands
@client.on(events.NewMessage(pattern=r'\.kick'))
async def kick(event):
    if not (event.is_group or event.is_channel):
        return await event.reply("❗ Yeh command sirf group me kaam karega.")
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("⚠️ Kisi user ko reply karo jise kick karna hai.")
    user = await replied.get_sender()
    try:
        await client.kick_participant(event.chat_id, user.id)
        await event.reply(f"👢 Kicked {user.first_name}")
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")

@client.on(events.NewMessage(pattern=r'\.ban'))
async def ban(event):
    if not (event.is_group or event.is_channel):
        return await event.reply("❗ Yeh command sirf group me kaam karega.")
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("⚠️ Kisi user ko reply karo jise ban karna hai.")
    user = await replied.get_sender()
    try:
        await client(functions.channels.EditBannedRequest(
            channel=event.chat_id,
            participant=user.id,
            banned_rights=types.ChatBannedRights(
                until_date=None,
                view_messages=True
            )
        ))
        await event.reply(f"🚫 Banned {user.first_name}")
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")

@client.on(events.NewMessage(pattern=r'\.mute'))
async def mute(event):
    if not (event.is_group or event.is_channel):
        return await event.reply("❗ Yeh command sirf group me kaam karega.")
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("⚠️ Kisi user ko reply karo jise mute karna hai.")
    user = await replied.get_sender()
    try:
        await client(functions.channels.EditBannedRequest(
            channel=event.chat_id,
            participant=user.id,
            banned_rights=types.ChatBannedRights(
                send_messages=True,
                until_date=None
            )
        ))
        await event.reply(f"🔇 Muted {user.first_name}")
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")

# Help command
@client.on(events.NewMessage(pattern=r'\.helpme'))
async def help_cmd(event):
    commands = """
🛠️ **UserBot Commands**:
• `.ping` – Test bot status
• `.alive` – Check if bot is alive
• `.id` – Your Telegram ID
• `.me` – Your profile info
• `.info` – Info of replied user
• `.kick` – Kick replied user
• `.ban` – Ban replied user
• `.mute` – Mute replied user
• `.helpme` – Show this help
"""
    await event.reply(commands)

# Main
async def main():
    print("Userbot is running...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
