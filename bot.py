import os
import logging
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment from .env (optional) then from environment variables.
load_dotenv()
# Load secrets from environment variables for safety. Do not commit real tokens.
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

if not TOKEN:
    raise RuntimeError("TOKEN environment variable is not set. See README.md for setup instructions.")

if not ADMIN_ID:
    raise RuntimeError("ADMIN_ID environment variable is not set. See README.md for setup instructions.")

try:
    ADMIN_ID = int(ADMIN_ID)
except Exception:
    logger.warning("ADMIN_ID not an integer; using as-is (string).")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tugma
    button = KeyboardButton("📱 Raqamni yuborish", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)

    # Startdagi xabar (emoji qo‘shilgan)
    await update.message.reply_text(
        "✨ Salom! Bu Gold Premium boti.\n\n"
        "📞 Siz bilan bog‘lanishimiz uchun pastdagi "
        "“Raqamni yuborish” tugmasini bosing.\n\n"
        "Biz sizga aloqaga chiqamiz yoki Telegramdan yozamiz!",
        reply_markup=markup
    )


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user  # Username olish uchun

    first_name = getattr(contact, "first_name", "-")
    last_name = getattr(contact, "last_name", "-")
    phone = getattr(contact, "phone_number", "-")
    user_id = getattr(contact, "user_id", "-")
    username = f"@{user.username}" if getattr(user, "username", None) else "-"

    text = (
        "📩 Yangi foydalanuvchi raqam yubordi!\n\n"
        f"👤 Ism: {first_name}\n"
        f"📛 Familiya: {last_name}\n"
        f"📱 Raqam: {phone}\n"
        f"🆔 User ID: {user_id}\n"
        f"🔗 Username: {username}"
    )

    # Admin (sizga) yuborish
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    # Foydalanuvchiga javob
    await update.message.reply_text("👍 Raqamingiz qabul qilindi! Tez orada aloqaga chiqamiz.")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    logger.info("Bot started. Polling...")
    app.run_polling()


if __name__ == "__main__":
    main()

