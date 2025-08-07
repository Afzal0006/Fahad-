import re
import json
import zipfile
import tempfile
import os
from telegram import Update, Document
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "Your Bot Token Here"

VIP_START = (
    "🔐 VIP Area: Netflix Cookies\n\n"
    "Welcome. Paste or upload your file.\n"
    "Your exclusive .txt file will be sent privately."
)

def extract_cookies(text):
    cookies = set()
    
    # Case 1: JSON format
    try:
        js = json.loads(text)
        if isinstance(js, list):
            netflixid, securenetflixid = None, None
            for entry in js:
                if isinstance(entry, dict):
                    if entry.get("name") == "NetflixId":
                        netflixid = entry.get("value")
                    if entry.get("name") == "SecureNetflixId":
                        securenetflixid = entry.get("value")
                    if netflixid and securenetflixid:
                        if netflixid != "" and securenetflixid != "":
                            cookies.add(f"NetflixId={netflixid}; SecureNetflixId={securenetflixid}")
                        netflixid, securenetflixid = None, None
            if cookies:
                return list(cookies)
    except Exception:
        pass

    # Case 2: Netscape format
    netscape_lines = text.splitlines()
    for idx, line in enumerate(netscape_lines):
        if "\tNetflixId\t" in line or "\tNetflixId " in line:
            nid = line.strip().split()[-1]
            for j in range(idx+1, min(idx+5, len(netscape_lines))):
                if "\tSecureNetflixId\t" in netscape_lines[j] or "\tSecureNetflixId " in netscape_lines[j]:
                    sid = netscape_lines[j].strip().split()[-1]
                    if nid != "" and sid != "":
                        cookies.add(f"NetflixId={nid}; SecureNetflixId={sid}")
    if cookies:
        return list(cookies)

    # Case 3: Regex search
    reg = re.compile(
        r'NetflixId\s*=\s*([v%3D0-9A-Za-z._\-]+).*?SecureNetflixId\s*=\s*([v%3D0-9A-Za-z._\-]+)', re.DOTALL)
    for m in reg.finditer(text):
        n, s = m.group(1), m.group(2)
        if n and s and n != "=" and s != "=":
            cookies.add(f"NetflixId={n}; SecureNetflixId={s}")

    # Case 4: Line-by-line scanning
    lines = text.splitlines()
    n, s = None, None
    for line in lines:
        if "NetflixId=" in line and "SecureNetflixId=" in line:
            n_match = re.search(r'NetflixId=([^\s;|]+)', line)
            s_match = re.search(r'SecureNetflixId=([^\s;|]+)', line)
            if n_match and s_match and n_match.group(1) and s_match.group(1):
                cookies.add(f"NetflixId={n_match.group(1)}; SecureNetflixId={s_match.group(1)}")
        else:
            if "NetflixId=" in line:
                n_match = re.search(r'NetflixId=([^\s;|]+)', line)
                if n_match:
                    n = n_match.group(1)
            if "SecureNetflixId=" in line:
                s_match = re.search(r'SecureNetflixId=([^\s;|]+)', line)
                if s_match:
                    s = s_match.group(1)
            if n and s:
                cookies.add(f"NetflixId={n}; SecureNetflixId={s}")
                n, s = None, None
    return list(cookies)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(VIP_START, reply_to_message_id=update.message.message_id)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await extract_and_send(update, update.message.text or "")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file: Document = update.message.document
    filename = file.file_name.lower()
    file_obj = await file.get_file()
    file_bytes = await file_obj.download_as_bytearray()

    # If ZIP file
    if filename.endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmpdir:
            zippath = os.path.join(tmpdir, "upload.zip")
            with open(zippath, "wb") as f:
                f.write(file_bytes)
            cookies = set()
            with zipfile.ZipFile(zippath, 'r') as zipf:
                for name in zipf.namelist():
                    if name.lower().endswith(('.txt', '.json', '.log', '.cookie', '.co', '.conf', '.ini')):
                        try:
                            data = zipf.read(name)
                            text = data.decode(errors="ignore")
                            extracted = extract_cookies(text)
                            cookies.update(extracted)
                        except Exception:
                            continue
            await output_cookies(update, cookies, reply_to=update.message.message_id)
            return

    # If regular file
    text = file_bytes.decode(errors="ignore")
    await extract_and_send(update, text)

async def extract_and_send(update: Update, text: str):
    extracting = await update.message.reply_text(
        "Extracting cookies... ⏳",
        reply_to_message_id=update.message.message_id
    )
    cookies = extract_cookies(text)
    await output_cookies(update, cookies, reply_to=update.message.message_id)
    await extracting.delete()

async def output_cookies(update: Update, cookies, reply_to=None):
    file_content = "\n".join(cookies) if cookies else "No cookies found."
    filename = "Le Re Lund Ke Cleaned Cookies.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)
    await update.message.reply_document(
        document=open(filename, "rb"),
        reply_to_message_id=reply_to
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()

if __name__ == "__main__":
    main()
