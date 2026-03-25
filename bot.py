from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import smtplib
import logging

# CONFIG
TOKEN = "8757888662:AAEc6AXEkfCdRcIZ33ByFHkAjkyddo73CFE"
EMAIL = "emailkamu@gmail.com"
PASSWORD = "APP_PASSWORD_GMAIL"
SMTP_SERVER = "MAIL.DOMAINKAMU.COM"
SMTP_PORT = 587

AUTHORIZED_USERS = [6694565529]  # ganti dengan ID Telegram kamu

# LOGGING
logging.basicConfig(level=logging.INFO)

# FUNCTION CEK USER
def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

# FUNCTION KIRIM EMAIL
def send_email(to_email, subject, body):
    msg = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, to_email, msg)
    server.quit()

# COMMAND START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif ✅")

# COMMAND SEND
async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_authorized(user_id):
        await update.message.reply_text("Akses ditolak ❌")
        return

    try:
        to_email = context.args[0]
        subject = context.args[1]
        body = " ".join(context.args[2:])

        send_email(to_email, subject, body)
        await update.message.reply_text("Email terkirim ✅")

    except:
        await update.message.reply_text("Format salah!\n/send email subject pesan")

# COMMAND BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_authorized(user_id):
        await update.message.reply_text("Akses ditolak ❌")
        return

    try:
        emails = context.args[0].split(",")
        subject = context.args[1]
        body = " ".join(context.args[2:])

        for email in emails:
            send_email(email.strip(), subject, body)

        await update.message.reply_text("Broadcast berhasil 🚀")

    except:
        await update.message.reply_text("Format:\n/broadcast email1,email2 subject pesan")

# INIT BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("send", send))
app.add_handler(CommandHandler("broadcast", broadcast))

print("Bot berjalan...")
app.run_polling()