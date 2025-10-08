import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai
import asyncio

# --- API Keys ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# --- Gemini setup ---
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Flask app (for webhook) ---
app = Flask(__name__)

# --- Telegram App setup ---
tg_app = Application.builder().token(TELEGRAM_TOKEN).build()

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm your Gemini AI bot. Type anything to chat.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_msg = update.message.text
        response = model.generate_content(user_msg)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Error: " + str(e))

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# --- Webhook Route ---
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), tg_app.bot)
    asyncio.run(tg_app.process_update(update))
    return "OK", 200

@app.route("/")
def home():
    return "Gemini Telegram Bot is Alive!"

# --- Start server ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TELEGRAM_TOKEN}"
    tg_app.bot.set_webhook(url=webhook_url)
    app.run(host="0.0.0.0", port=port)        except Exception as e:
            reply = "Error: " + str(e)

        # Telegram message length limit protection
        bot.send_message(chat_id, reply[:4000])

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
