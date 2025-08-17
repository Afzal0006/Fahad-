import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 24024383
API_HASH = "e4defcf520c9333e56196378440e990c"
STRING_SESSION = "AQFulT8AGz5gsKX_sr74eR9CahbNukSh-DNg5wRAOSBEByClXwn960S-6OV1aYE8ZK0hpq_FXwKEvvGb2-ZeVpnj3cSyQLWHueUGAwKtH0rtVBY3pJJORnShhYKZdBn0XIoTtgnCtxtCCF1BipDtJtStN1aIvR9_Gt5VZjVzrcrFpZHJrKhGaR7Kjvfl_ntI2xhdw9bQF19Ne8DaXVijwjfb2dCipbx1Ms8Inybrkh69Qyz-aFN9ckY4aFm0WLm8R-DnqwvL70A8cefw_p7uy02SdeGHNZIAWXsbZV49LtMq3n6uC1auRW-QwfMktBkYAiYfIcBuYfEx7G1VtlM1w3IrAU2szAAAAAG0N0VUAA"

user = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

@user.on_message(filters.command("acceptall") & filters.me)
async def accept_all(client: Client, message: Message):
    chat_id = message.chat.id
    count = 0
    await message.reply_text("⏳ Approving all pending join requests...")
    async for req in client.get_chat_join_requests(chat_id):
        try:
            await client.approve_chat_join_request(chat_id, req.from_user.id)
            count += 1
            await asyncio.sleep(random.randint(8, 12))  # safe delay
        except Exception as e:
            print("Error:", e)
    await message.reply_text(f"🎉 Done! Approved {count} requests.")

print("🚀 Userbot started. Type /acceptall in your group to approve requests.")
user.run()
