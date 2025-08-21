from pyrogram import Client, filters

API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
STRING_SESSION = "BQF3VRIAtGq62TIJk_839dTKKhWXoHS4V-zNRzpLMMb4WSvJpvPba4Xz9MF9iCKHrtfZwhBTO1fkDYMvP5blTUILk_CCGg5cEkB9ZI4ImkNWbc7AheNqJ8N60gzdw94j7SOGtUYsodXullKWWupZ3l9qkj66P4osKNuwXwFfx3TdFpfOAIMAZdPbordQFmuQc7sAXzNr3LzrCzx2usko1TGN2fIrbmgTc0ECGXFGKh__7gBioJjIYdBbPoj_f3Zblh0vS-CW0LPNr-PRAuGRJ1bB-y1qpojXdP-6RkkvaRf99YgcJjt18vjWOo3_T6t8Q4pWn1YAZvNC63a7XVJzPGUj1cBhwAAAAAGAPjyTAA"

app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

@app.on_message(filters.private & filters.text)
async def create_group(client, message):
    try:
        if message.text.lower() in ["deal", "/setup", "/create"]:
            chat_title = f"Escrow Deal - {message.from_user.first_name}"

            # Step 1: Create a private supergroup
            group = await client.create_supergroup(chat_title, "Private escrow group auto-created")

            # Step 2: Add the user to the group
            await client.add_chat_members(group.id, [message.from_user.id])

            # Step 3: Generate and send the invite link
            link = await client.export_chat_invite_link(group.id)
            await message.reply_text(f"✅ New private escrow group created:\n🔗 {link}")
        else:
            await message.reply_text("Type 'deal' or '/setup' to create a new escrow group.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

print("🚀 Userbot running...")
app.run()
