from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import time

# === CONFIG ===
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
STRING_SESSION = "BQF3VRIAczuxK1ipcqX2JfGknnnVEfHUlkimCICjvgNjfzbiqw7hsnacLpX-natIy8H8nNWEqQJIOHInD0Scy-bzlb3e_ELSu4Vj89zdJSMARA-zQMcDimoP-LhAz-EjQ8J478OXQ3b8zrekvpMBP182K9daYcGI5n9_49eAsA8hQ5WwAz95Wfv95wrV-ZQkIFMRTAYAIqkHBa6zAyktw29Tfrtkv4fb26kFxkhbY4Q9fcMCr1MLDFxjDYxtx_N15bCK4M-5lAckgfL5k6La1XstSDr0JAY9r8i7JB5tl8SLsVbf0ziTtk2uDsY2S2ZOPzgJPY3rZeDxt7a5AHOcTMzHWJeFHQAAAAGAPjyTAA"
ESCROW_BOT_USERNAME = "DemoEscrowerBot"  # without @
OWNER_ID = 7278904232  # Apna Telegram user ID yaha daal

# === START CLIENT ===
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

@app.on_message(filters.private & filters.text)
async def create_group(client, message):
    trigger_words = ["deal", "/setup", "/create"]

    if message.text.lower() in trigger_words:
        try:
            buyer_username = (
                f"@{message.from_user.username}" 
                if message.from_user.username 
                else message.from_user.first_name
            )

            chat_title = f"Escrow Deal - {message.from_user.first_name}"

            # Step 1: Create private supergroup
            group = await client.create_supergroup(chat_title, "Private escrow group auto-created")

            # Step 2: Add buyer
            await client.add_chat_members(group.id, message.from_user.id)

            # Step 3: Add owner
            await client.add_chat_members(group.id, OWNER_ID)

            # Step 4: Add escrow bot
            await client.add_chat_members(group.id, ESCROW_BOT_USERNAME)

            # Step 5: Send and pin the form
            form_message = f"""
**DEAL INFO :**
**BUYER :** @
**SELLER :** @
**DEAL AMOUNT :** 10 rs
**TIME TO COMPLETE DEAL :**
"""
            sent_msg = await client.send_message(group.id, form_message)
            await client.pin_chat_message(group.id, sent_msg.id)

            # Step 6: Send invite link to buyer
            link = await client.export_chat_invite_link(group.id)
            await message.reply_text(f"✅ New private escrow group created:\n🔗 {link}")

        except FloodWait as e:
            time.sleep(e.value)
            await message.reply_text("⏳ Please try again later, Telegram rate limit reached.")

        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    else:
        await message.reply_text("Type 'deal' or '/setup' to create a new escrow group.")

print("🚀 Userbot running...")
app.run()
