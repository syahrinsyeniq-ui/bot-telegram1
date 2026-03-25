import os
import logging
import smtplib
from email.mime.text import MIMEText

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ================= CONFIG =================
TOKEN = os.getenv("8757888662:AAEc6AXEkfCdRcIZ33ByFHkAjkyddo73CFE")
EMAIL = os.getenv("donotreply@register-scmoontonn.com")
PASSWORD = os.getenv("n4rIx(D5c9uX7]")

SMTP_SERVER = os.getenv("SMTP_SERVER", "asia.emailarray.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

AUTHORIZED_USERS = [66945655]  # ganti dengan ID kamu

# ================= LOG =================
logging.basicConfig(level=logging.INFO)

# ================= TEMPLATE PESAN =================
def get_auto_message():
    return """
Halo,

Ini adalah pesan otomatis dari sistem.

Mohon abaikan jika tidak relevan dengan Anda.

Terima kasih.
"""

# ================= CEK USER =================
def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

# ================= SEND EMAIL =================
def send_email(to_email):
    subject = "Notifikasi Sistem"
    body = get_auto_message()

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        logging.error(e)
        return False

# ================= COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot aktif ✅\nGunakan:\n/send email@tujuan.com"
    )


async def send_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_authorized(user_id):
        await update.message.reply_text("❌ Akses ditolak")
        return

    try:
        to_email = context.args[0]

        success = send_email(to_email)

        if success:
            await update.message.reply_text("✅ Email terkirim")
        else:
            await update.message.reply_text("❌ Gagal kirim email")

    except:
        await update.message.reply_text(
            "Format salah!\n/send email@tujuan.com"
        )

# ================= RUN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send_cmd))

    print("Bot berjalan...")
    app.run_polling()

if name == "__main__":
    main()
