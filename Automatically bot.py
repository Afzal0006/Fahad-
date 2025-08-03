import os
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pyrogram import Client as UserClient

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", 123456))
API_HASH = os.getenv("API_HASH", "your_api_hash")
STRING_SESSION = os.getenv("BQGM8vsAuzqnG4-RM6mft9DZfDPGAJhvcJp5GA9sQdJj6uc9yWXiBeAj4YyYyGpd4V3oq-ZVy0DoT-7enLyXi_K_SUEu7-WnW0dw4iP37V8yltfyh_aR6CUkpa-325Arz91Ct9lfV7FnacS8_AE6YSsc5nU3gaKt3ZSHfil8n95Gh0gZ14PgWYG_n1j_iv7rWykU39oz-TNH93a4hYbWkzFYuQFAtYgo3nB82WYcn2TxBCYYixmEXW4F1uyezZ0usaECSgtuI3xTjsbq3ogXKAI4xJhd8kTVp1pQIk0ryZ0TFbdlGj50gWqdcuVzU8c1zA34KcbDusUOlS2Qi8tApoVExduhPQAAAAGx20OoAA", "your_string_session")

userbot = UserClient(
    name="userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Type /deal to create a private group.")

async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        async with userbot:
            group = await userbot.create_supergroup(title=f"Deal with {user.first_name}")
            link = await userbot.export_chat_invite_link(group.id)
        await update.message.reply_text(f"✅ New private group created!\nJoin here: {link}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        logger.error(e)

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deal", deal))
    app.run_polling()
