from pyrogram import Client, filters

API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"
BOT_ID = 8414351117

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

@app.on_message(filters.private & filters.from_user(BOT_ID))
async def handle_create(client, message):
    if message.text.strip().lower() == "/create":
        chat = await client.create_supergroup("Escrow Deal", "This is an escrow group.")
        link = await client.export_chat_invite_link(chat.id)
        await client.send_message(BOT_ID, link)

app.run()
