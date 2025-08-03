import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "-1001234567890"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Type /deal to get your private deal group link.")

async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        link = await context.bot.create_chat_invite_link(
            chat_id=GROUP_ID,
            member_limit=1,
            creates_join_request=False
        )
        await update.message.reply_text(f"✅ Here is your private deal group link:\n{link.invite_link}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        logger.error(e)

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deal", deal))
    app.run_polling()
