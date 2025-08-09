import asyncio
from datetime import datetime
from pyrogram import Client, filters

API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"

OWNER_ID = 6998916494  # Aapka Telegram User ID

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

broadcast_task = None
stop_broadcast = False

COMMANDS = {
    "/stats": "Chat/group ke stats dikhata hai.",
    "/join": "Group ya channel join karta hai. Usage: /join <invite_link_or_username>",
    "/leave": "Group ya channel chhodta hai. Usage: /leave <chat_id_or_username>",
    "/broadcast": "Sab chats me message bhejta hai. Usage: /broadcast {seconds} <message>",
    "/stop": "Periodic broadcast ko rokta hai.",
    "/ping": "Bot ki speed aur current time check karta hai.",
    "/help": "Commands list dikhata hai."
}

def owner_only(func):
    async def wrapper(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply("If u want to use this bot contact with @golgibody")
        return await func(client, message)
    return wrapper

@app.on_message(filters.command("help") & filters.me)
@owner_only
async def help_cmd(client, message):
    help_text = "**Available Commands:**\n\n"
    for cmd, desc in COMMANDS.items():
        help_text += f"`{cmd}` : {desc}\n"
    await message.reply(help_text)

@app.on_message(filters.command("stats") & filters.me)
@owner_only
async def stats_cmd(client, message):
    chat = message.chat
    total_members = getattr(chat, "members_count", 0)
    if total_members == 0 and chat.type in ["group", "supergroup", "channel"]:
        total_members = 0
        async for member in client.iter_chat_members(chat.id):
            total_members += 1
    text = (
        f"Chat Title: {chat.title or 'N/A'}\n"
        f"Chat Type: {chat.type}\n"
        f"Chat ID: {chat.id}\n"
        f"Total Members: {total_members}"
    )
    await message.reply(text)

@app.on_message(filters.command("join") & filters.me)
@owner_only
async def join_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /join <invite_link_or_username>")
    link = message.command[1]
    try:
        await client.join_chat(link)
        await message.reply(f"Successfully joined {link}")
    except Exception as e:
        await message.reply(f"Failed to join: {e}")

@app.on_message(filters.command("leave") & filters.me)
@owner_only
async def leave_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /leave <chat_id_or_username>")
    chat_to_leave = message.command[1]
    try:
        await client.leave_chat(chat_to_leave)
        await message.reply(f"Left chat {chat_to_leave}")
    except Exception as e:
        await message.reply(f"Failed to leave: {e}")

async def periodic_broadcast(client, message_text, delay):
    global stop_broadcast
    stop_broadcast = False
    try:
        while not stop_broadcast:
            sent = 0
            failed = 0
            async for dialog in client.get_dialogs():
                try:
                    await client.send_message(dialog.chat.id, message_text)
                    sent += 1
                except Exception:
                    failed += 1
            print(f"Broadcast sent to {sent} chats, failed in {failed} chats.")
            await asyncio.sleep(delay)
    except asyncio.CancelledError:
        print("Broadcast task cancelled")
        raise

@app.on_message(filters.command("broadcast") & filters.me)
@owner_only
async def broadcast_cmd(client, message):
    global broadcast_task, stop_broadcast

    if len(message.command) < 3:
        return await message.reply("Usage: /broadcast {seconds} <message>")

    delay_part = message.command[1]
    if delay_part.startswith("{") and delay_part.endswith("}"):
        try:
            delay_seconds = int(delay_part[1:-1])
        except ValueError:
            return await message.reply("Delay must be an integer inside curly braces. Example: {60}")
    else:
        return await message.reply("Delay should be in format {seconds}, e.g. {60}")

    broadcast_message = message.text.split(None, 2)[2]

    if broadcast_task and not broadcast_task.done():
        stop_broadcast = True
        broadcast_task.cancel()
        try:
            await broadcast_task
        except asyncio.CancelledError:
            pass
        await asyncio.sleep(1)

    broadcast_task = app.loop.create_task(periodic_broadcast(client, broadcast_message, delay_seconds))
    await message.reply(f"Started periodic broadcast every {delay_seconds} seconds.")

@app.on_message(filters.command("stop") & filters.me)
@owner_only
async def stop_cmd(client, message):
    global broadcast_task, stop_broadcast
    if broadcast_task and not broadcast_task.done():
        stop_broadcast = True
        broadcast_task.cancel()
        try:
            await broadcast_task
        except asyncio.CancelledError:
            pass
        await message.reply("Periodic broadcast stopped.")
    else:
        await message.reply("No periodic broadcast is running.")

@app.on_message(filters.command("ping") & filters.me)
@owner_only
async def ping_cmd(client, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.reply(f"Pong! 🏓\nTime: {now}")

print("Bot is starting...")
app.run()
