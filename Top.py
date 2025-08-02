from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import g4f

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# User conversation memory
user_memory = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hi! I am your Free AI Chat Bot.\n"
        "💬 Just type anything and I will reply!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Initialize memory for new users
    if user_id not in user_memory:
        user_memory[user_id] = []

    # Store user message
    user_memory[user_id].append({"role": "user", "content": user_text})

    # Keep only last 10 messages per user
    if len(user_memory[user_id]) > 10:
        user_memory[user_id] = user_memory[user_id][-10:]

    try:
        # Get AI reply from g4f (free)
        response = g4f.ChatCompletion.create(
            model="gpt-4",  # Can use "gpt-3.5-turbo" also
            messages=user_memory[user_id]
        )
        bot_reply = response

        # Save bot reply in memory
        user_memory[user_id].append({"role": "assistant", "content": bot_reply})

        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Free ChatGPT Bot started successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
