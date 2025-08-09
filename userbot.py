from pyrogram import Client, filters

API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"

OWNER_IDS = [1446846502, 6998916494]  # Replace with your Telegram user IDs

app = Client(
    "my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

@app.on_message(filters.private & filters.command("join"))
def join_group(client, message):
    if message.from_user.id not in OWNER_IDS:
        message.reply_text("🚫 You don't have permission to use this command.")
        return

    if len(message.command) < 2:
        message.reply_text(
            "❌ Usage: /join <group invite link or username>\n\n"
            "Example:\n"
            "/join https://t.me/joinchat/abcdefg1234567\n"
            "/join @groupusername"
        )
        return

    group = message.command[1]
    try:
        client.join_chat(group)
        message.reply_text(f"✅ Successfully joined: {group}")
    except Exception as e:
        message.reply_text(f"❌ Error while joining:\n{e}")

print("Userbot is running... Press Ctrl+C to stop.")
app.run()
