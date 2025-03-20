import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai

# Load API keys from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Store conversation history
chat_history = []

def chat(update: Update, context: CallbackContext):
    """Handle user messages and respond with ChatGPT while remembering history"""
    user_message = update.message.text

    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_message})

    # Send chat history to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=chat_history
    )

    bot_reply = response.choices[0].message.content

    # Add bot response to chat history
    chat_history.append({"role": "assistant", "content": bot_reply})

    # Send reply to Telegram
    update.message.reply_text(bot_reply)

# Initialize bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Add message handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Start bot
app.run_polling()
