from pyrogram import Client, filters

API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"

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
