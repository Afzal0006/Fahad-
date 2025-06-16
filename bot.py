from telethon import TelegramClient, events
import asyncio

# Replace these with your own values
API_ID = 28327193
API_HASH = '4aa7d6f0ae2f65fc8c80c69f03d00ae1'
SESSION_NAME = 'BQGwPRkAKOB08pWhlQn1BwiNMK8RlTaBp6CVphq76CC447VIYi63CcRU1qd61BfdwiR1anqvicoEjN8Dti73Mir6ohVYT81ZBeMiy4ccN1eg4MVQA9toGV3PXIhsZ7bIblIMg0_5OJ07Uvpx5_HeGhG6Q8_kmBX0snL18cieMbIXbO3q5RXF-Pc3ZwY-AY2rfiqIcFU0SuglSp0yGYOM7l4PsCoUCjd1ELcWIb-NnO3bThCdMhMaLV19QKNLeIoZqlnIq_9idDkmq4t9b7Mt9Yf7ZMFUmlYtstND65GfSUZb2iUGBO76yl57BBMdqmNSKauCP49jAoQ8DOri3-a79OGiIitbyAAAAAHceB2jAA'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'\.ping'))
async def ping(event):
    await event.reply("🏓 Pong!")

async def main():
    print("Userbot is running...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
