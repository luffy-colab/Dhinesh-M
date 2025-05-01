import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Set your tokens here
TELEGRAM_BOT_TOKEN = "7932747849:AAGmctroqL4zsj-goO_TgKsgWPoEtA2sen0"
NUMVERIFY_API_KEY = "5aa4f988a6cd9b0687cff9e4dd019f24"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a phone number with country code (e.g. +14158586273).")

async def lookup_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    if not number.startswith('+'):
        await update.message.reply_text("Include country code. Example: +14158586273")
        return

    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={number}"
    try:
        response = requests.get(url).json()
    except Exception as e:
        await update.message.reply_text("Error fetching info.")
        logger.error(f"API error: {e}")
        return

    if response.get("valid"):
        reply = (
            f"📞 Number: {response['international_format']}\n"
            f"🌍 Country: {response['country_name']} ({response['country_code']})\n"
            f"📱 Carrier: {response['carrier']}\n"
            f"📡 Line Type: {response['line_type']}\n"
            f"🧭 Location: {response.get('location', 'N/A')}"
        )
    else:
        reply = "❌ Invalid number or not found."

    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lookup_number))

    print("✅ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
