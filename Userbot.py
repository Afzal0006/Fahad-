from telethon import TelegramClient, events

API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
SESSION = "BQGM8vsALiR2AWik4SWrvYlsaRw9hdOF82r43DkMpxY9QyxZn3s1dSfff7vUeyN_SrcoJESXDSSwtWx2wnv_F7hzeEKuFRh6C_VnmTChySSxagfKdV7tQvCgz0sOFxiSvUipmsLod7rSxTC8OUM35KGV4bjyvRewPO-WhPlYFsnQUxoG4dOxNHW9MwDr-UToR097V5byYZryELXttdF4NlycFKZo34Gs6qGnpQ08M887g9Bc4cr-eA6iq-_9qx_BCGSiHGL8SLkS25XAmio5AMnPBOatKUqQNBW_BbAr9KXOjtV2uJRXx6znm08TmEB45iD_rzyvQkT1SrNcSknR0RDA8lAFDgAAAAGx20OoAA"

client = TelegramClient(SESSION, API_ID, API_HASH)

@client.on(events.NewMessage(pattern="^/ping$"))
async def ping(event):
    if event.is_group:
        admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=client.iter_admins)]
        if event.sender_id in admins:
            await event.reply("Pong! ✅")

client.start()
client.run_until_disconnected()
