from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, ContextTypes

# Ban command
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a user's message to ban them!")
        return

    user_id = update.message.reply_to_message.from_user.id
    try:
        await update.effective_chat.ban_member(user_id)
        await update.message.reply_text("✅ User has been banned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to ban user: {e}")

# Mute command
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a user's message to mute them!")
        return

    user_id = update.message.reply_to_message.from_user.id
    try:
        await update.effective_chat.restrict_member(
            user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text("🔇 User has been muted!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to mute user: {e}")

def main():
    TOKEN = "8358410115:AAF6mtD7Mw1YEn6LNWdEJr6toCubTOz3NLg"  # Your bot token

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))

    print("✅ Bot started and running...")
    app.run_polling()

if __name__ == "__main__":
    main()
