from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "7969208313:AAFRA-tbEvSTFlU1ESxTeMmn1yDk5OLOSDQ"

# -------- /banall command --------
async def ban_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    # Check if command is in a group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ Yeh command sirf groups me kaam karegi!")
        return

    # Check if user is admin
    member = await chat.get_member(user.id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("❌ Sirf admin hi /banall chala sakta hai!")
        return

    await update.message.reply_text("⚠️ Ban All Started... Group ke sare members ban kiye ja rahe hai.")

    # Iterate over all members
    async for member in chat.get_members():
        try:
            # Skip admins, creator & bot
            if member.status in ["administrator", "creator"] or member.user.is_bot:
                continue

            await chat.ban_member(member.user.id)
        except Exception as e:
            print(f"Error banning {member.user.id}: {e}")

    await update.message.reply_text("✅ Ban All Complete! Sare members ban ho gaye.")

# -------- Start Command --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 BanAll Bot Ready!\nUse /banall in group (admin only).")

# -------- Main Function --------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("banall", ban_all))

    print("✅ Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
