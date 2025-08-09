from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot credentials
API_ID = 20917743
API_HASH = "0e8bcef16b3bae4f852bf42775f04ace"
BOT_TOKEN = "8414351117:AAEDEkc1VblJ8NU8Umle1gby1KyY94Gd1x4"

bot = Client(
    "fancy_write_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Fancy font converter
def to_fancy(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fancy = "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"
    return text.translate(str.maketrans(normal, fancy))

@bot.on_message(filters.command(["write", "Write"], prefixes=["/", ".", "!", "?"]))
async def fancy_handler(client, message):
    args = message.text.split(None, 1)
    
    if len(args) < 2:
        await message.reply_text("Usage: /write <text>\nExample: /write Hello world", quote=True)
        return
    
    text_to_send = args[1]
    fancy_text = to_fancy(text_to_send)

    # Copy button
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📋 Copy to input", switch_inline_query_current_chat=fancy_text)]]
    )

    await message.reply_text(fancy_text, reply_markup=btn, quote=True)

if __name__ == "__main__":
    print("Fancy Font Write Bot started...")
    bot.run()
