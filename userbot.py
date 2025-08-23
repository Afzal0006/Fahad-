from pyrogram import Client, filters

API_ID = 21081718
API_HASH = "fec3c59a0f36beb71199dba4459eef86"
STRING_SESSION = "BQFBrnYAl-pWnXbngB408FvSpoCaD7zojyTEPq9HUho4f_6juAcAzJ7TuF0v2TCZ0ahvEsEHjHhxWxyq9VbYwCh1mfUQvtHiy6WLaSor8F0g_jaz07f-W8_Gy6NQLiEJt_YXrhy4Py0L6MnTSxb4U_Xn4PWlQQ934BD-nh8BxyCgTV_DcQrvA8YwpWDGeKem1ZaAK8lQvtcCj5jmNs4WBHNSXchphObU_MxfZm_-lKCABX3CYY_I_CIyNMQH9WUIp2syavT-9iakCWa8WtMN-NFrxPc6LX14KxveI24ZmGeBj2_bwxWTDrzrJj4ppYiGZ6Xvo06tAlKkmFY4bihnqvTPgbopYAAAAAGxU39QAA"

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
