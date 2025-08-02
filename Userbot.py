from pyrogram import Client

app = Client(
    "userbot",
    api_id=26014459,
    api_hash="34b8791089c72367a5088f96d925f989",
    session_string="BQGM8vsALiR2AWik4SWrvYlsaRw9hdOF82r43DkMpxY9QyxZn3s1dSfff7vUeyN_SrcoJESXDSSwtWx2wnv_F7hzeEKuFRh6C_VnmTChySSxagfKdV7tQvCgz0sOFxiSvUipmsLod7rSxTC8OUM35KGV4bjyvRewPO-WhPlYFsnQUxoG4dOxNHW9MwDr-UToR097V5byYZryELXttdF4NlycFKZo34Gs6qGnpQ08M887g9Bc4cr-eA6iq-_9qx_BCGSiHGL8SLkS25XAmio5AMnPBOatKUqQNBW_BbAr9KXOjtV2uJRXx6znm08TmEB45iD_rzyvQkT1SrNcSknR0RDA8lAFDgAAAAGx20OoAA"
)

@app.on_chat_join_request()
async def approve(client, join_request):
    await client.approve_chat_join_request(join_request.chat.id, join_request.from_user.id)
    print(f"Accepted: {join_request.from_user.id}")

app.run()
