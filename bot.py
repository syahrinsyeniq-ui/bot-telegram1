import os
import smtplib
from email.mime.text import MIMEText
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8757888662:AAEc6AXEkfCdRcIZ33ByFHkAjkyddo73CFE")

SMTP_HOST = os.getenv("asia.emailarray.com")
SMTP_PORT = int(os.getenv("587", 465))
SMTP_USER = os.getenv("donotreply@register-scmoontonn.com")
SMTP_PASS = os.getenv("Wawan460630!#")
SMTP_SECURE = os.getenv("tls", "ssl")

def send_email(to_email, message):
    msg = MIMEText(message)
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = "Pesan dari Bot"

    if SMTP_SECURE == "ssl":
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    else:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()

    server.login(SMTP_USER, SMTP_PASS)
    server.send_message(msg)
    server.quit()

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "|" not in text:
        await update.message.reply_text("Format: email@gmail.com|pesan")
        return

    email, pesan = text.split("|", 1)

    try:
        send_email(email, pesan)
        await update.message.reply_text("✅ Email terkirim")
    except:
        await update.message.reply_text("❌ Gagal kirim")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("Bot jalan...")
app.run_polling()
