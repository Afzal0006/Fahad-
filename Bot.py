import time
from telegram.ext import Updater, CommandHandler

# Bot token
BOT_TOKEN = "8358410115:AAF6mtD7Mw1YEn6LNWdEJr6toCubTOz3NLg"

# Bot ka start time
START_TIME = time.time()

def ping(update, context):
    # Current time - start time = uptime
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime = f"{hours}h {minutes}m {seconds}s"
    
    update.message.reply_text(f"🏓 Pong!\n⏳ Uptime: {uptime}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Ping command handler
    dp.add_handler(CommandHandler("ping", ping))

    print("✅ Bot Started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
