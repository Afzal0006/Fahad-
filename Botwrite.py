from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
import os

# ====== Your Bot Credentials ======
API_ID = 20917743
API_HASH = "0e8bcef16b3bae4f852bf42775f04ace"
BOT_TOKEN = "8414351117:AAEDEkc1VblJ8NU8Umle1gby1KyY94Gd1x4"
# ===================================

# Fancy font style
FANCY_STYLE = "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵" \
              "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"

# Convert normal text to fancy
def to_fancy(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return text.translate(str.maketrans(normal, FANCY_STYLE))

# Create blank slide with fancy text
def text_on_blank_slide(text, output_file="slide.png"):
    img = Image.new("RGB", (1280, 720), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    fancy_text = to_fancy(text)
    text_width, text_height = draw.textsize(fancy_text, font=font)
    x = (img.width - text_width) / 2
    y = (img.height - text_height) / 2

    draw.text((x, y), fancy_text, font=font, fill="black")
    img.save(output_file)
    return output_file

# Bot client
bot = Client(
    "fancy_write_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Command handler
@bot.on_message(filters.command("write", prefixes=["/", ".", "!", "?"], case_sensitive=False))
async def fancy_handler(client, message):
    args = message.text.split(None, 1)

    if len(args) < 2:
        await message.reply_text("Usage: /write <text>\nExample: /write Hello world", quote=True)
        return

    text_to_write = args[1]
    image_path = text_on_blank_slide(text_to_write)
    
    await message.reply_photo(image_path, caption="Here is your fancy text slide 🖼️")
    
    os.remove(image_path)  # Clean up

if __name__ == "__main__":
    print("Fancy Font Write Bot started...")
    bot.run()
