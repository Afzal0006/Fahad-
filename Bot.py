import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8358410115:AAF6mtD7Mw1YEn6LNWdEJr6toCubTOz3NLg"

# Random NFT images (URLs)
NFT_IMAGES = [
    "https://i.ibb.co/p0Zg1dp/nft1.png",
    "https://i.ibb.co/Mk3GHxW/nft2.png",
    "https://i.ibb.co/XVQQP0c/nft3.png",
]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌞 Good Morning! Welcome to my Bot.")

    # Inline buttons
    keyboard = [
        [
            InlineKeyboardButton("NFT", callback_data="nft"),
            InlineKeyboardButton("LOL", callback_data="lol")
        ],
        [
            InlineKeyboardButton("POP", callback_data="pop"),
            InlineKeyboardButton("Rose or Candy", callback_data="rose_candy")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose one:", reply_markup=reply_markup)

# Button press handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "nft":
        nft_url = random.choice(NFT_IMAGES)
        await query.message.reply_photo(photo=nft_url, caption="🖼️ Here is your NFT!")
    elif data == "lol":
        await query.edit_message_text("😂 LOL!!")
    elif data == "pop":
        await query.edit_message_text("🎉 POP POP POP!")
    elif data == "rose_candy":
        await query.edit_message_text("🌹 Here's a Rose and 🍬 Candy!")

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
