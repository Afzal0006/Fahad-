from pyrogram import Client, filters

# Apke credentials
api_id = 24597778
api_hash = "0b34ead62566cc7b072c0cf6b86b716e"
string_session = "BQF3VRIAtGq62TIJk_839dTKKhWXoHS4V-zNRzpLMMb4WSvJpvPba4Xz9MF9iCKHrtfZwhBTO1fkDYMvP5blTUILk_CCGg5cEkB9ZI4ImkNWbc7AheNqJ8N60gzdw94j7SOGtUYsodXullKWWupZ3l9qkj66P4osKNuwXwFfx3TdFpfOAIMAZdPbordQFmuQc7sAXzNr3LzrCzx2usko1TGN2fIrbmgTc0ECGXFGKh__7gBioJjIYdBbPoj_f3Zblh0vS-CW0LPNr-PRAuGRJ1bB-y1qpojXdP-6RkkvaRf99YgcJjt18vjWOo3_T6t8Q4pWn1YAZvNC63a7XVJzPGUj1cBhwAAAAAGAPjyTAA"

app = Client(session_name=string_session, api_id=api_id, api_hash=api_hash)

# Command /create {groupname} handle karna
@app.on_message(filters.me & filters.command("create", prefixes="/"))
async def create_supergroup(client, message):
    if len(message.command) < 2:
        await message.reply_text("Group ka naam provide karo. Usage: /create {groupname}")
        return

    group_name = " ".join(message.command[1:])
    
    try:
        # Supergroup create karna
        new_chat = await app.create_supergroup(title=group_name, description=f"Supergroup {group_name} created by userbot")
        await message.reply_text(f"✅ Supergroup created!\n\nTitle: {new_chat.title}\nID: {new_chat.id}")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

app.run()
