from pyrogram import Client, filters

app = Client("my_account")

@app.on_message(filters.command("ping") & filters.me)
async def ping(client, message):
    await message.reply_text("Pong!")

app.run()
