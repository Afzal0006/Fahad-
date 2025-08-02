FROM python:3.9-slim

# Install compiler and build tools for tgcrypto
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir pyrogram==2.0.106 tgcrypto pyaes==1.6.1 pysocks==1.7.1

# Add Python code directly into the image
RUN echo "\
from pyrogram import Client\n\
\n\
app = Client(\n\
    'userbot',\n\
    api_id=26014459,\n\
    api_hash='34b8791089c72367a5088f96d925f989',\n\
    session_string='BQGM8vsALiR2AWik4SWrvYlsaRw9hdOF82r43DkMpxY9QyxZn3s1dSfff7vUeyN_SrcoJESXDSSwtWx2wnv_F7hzeEKuFRh6C_VnmTChySSxagfKdV7tQvCgz0sOFxiSvUipmsLod7rSxTC8OUM35KGV4bjyvRewPO-WhPlYFsnQUxoG4dOxNHW9MwDr-UToR097V5byYZryELXttdF4NlycFKZo34Gs6qGnpQ08M887g9Bc4cr-eA6iq-_9qx_BCGSiHGL8SLkS25XAmio5AMnPBOatKUqQNBW_BbAr9KXOjtV2uJRXx6znm08TmEB45iD_rzyvQkT1SrNcSknR0RDA8lAFDgAAAAGx20OoAA'\n\
)\n\
\n\
@app.on_chat_join_request()\n\
async def approve(client, join_request):\n\
    await client.approve_chat_join_request(join_request.chat.id, join_request.from_user.id)\n\
    print(f'✅ Accepted Join Request: {join_request.from_user.id}')\n\
\n\
app.run()\n\
" > main.py

# Run the bot
CMD ["python", "main.py"]
