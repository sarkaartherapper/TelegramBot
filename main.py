from flask import Flask, request
import os
from google import genai
from telegram import Bot

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def home():
    return "Gemini Bot is running successfully on Render."

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if not text:
            bot.send_message(chat_id, "Please type something.")
            return "ok"

        try:
            # Call Gemini API
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text
            )
            reply = response.text or "No response from Gemini."
        except Exception as e:
            reply = "Error: " + str(e)

        # Telegram message length limit protection
        bot.send_message(chat_id, reply[:4000])

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)