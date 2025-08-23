from pyrogram import Client, filters

api_id = 21081718
api_hash = "fec3c59a0f36beb71199dba4459eef86"
string = "BQFBrnYAl-pWnXbngB408FvSpoCaD7zojyTEPq9HUho4f_6juAcAzJ7TuF0v2TCZ0ahvEsEHjHhxWxyq9VbYwCh1mfUQvtHiy6WLaSor8F0g_jaz07f-W8_Gy6NQLiEJt_YXrhy4Py0L6MnTSxb4U_Xn4PWlQQ934BD-nh8BxyCgTV_DcQrvA8YwpWDGeKem1ZaAK8lQvtcCj5jmNs4WBHNSXchphObU_MxfZm_-lKCABX3CYY_I_CIyNMQH9WUIp2syavT-9iakCWa8WtMN-NFrxPc6LX14KxveI24ZmGeBj2_bwxWTDrzrJj4ppYiGZ6Xvo06tAlKkmFY4bihnqvTPgbopYAAAAAGxU39QAA"

BOT_ID = 8350094964

userbot = Client(
    "userbot",
    api_id=api_id,
    api_hash=api_hash,
    session_string=string
)

@userbot.on_message(filters.command("escrow", prefixes=["/"]) & filters.user(BOT_ID))
async def create_group(_, message):
    chat = await userbot.create_group(
        title="🤝 Escrow Trade Group",
        users=[BOT_ID]
    )
    link = await userbot.export_chat_invite_link(chat.id)
    await message.reply_text(f"✅ Escrow group bana diya!\n\n🔗 {link}")

userbot.run()
