import asyncio
import os
from telegram.ext import CommandHandler, Application, MessageHandler, filters, ContextTypes
from telegram import Update
import random
from dotenv import load_dotenv
from expressions import text_to_list, text

load_dotenv()
bot = os.getenv('TOKEN')
bot_name = '@Hhhh_Tttt_bot'

quotes_list = text_to_list(text)
print(bot_name)

 # Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Привіт я бот в розробці, буду тебе мотивувати!!!\n\nОсь тобі мотиваційний вираз на сьогодні:\n\n{random.choice(quotes_list)}")
    
    
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Чим можу допомогти?")
    
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Це команда кастомна")
    
    
# Response

def handle_response(text: str) -> str:
    
    processed: str = text.lower()
    
    
    if "hello" in processed:
        return "Привіт, як твої справи?"
    
    if "how are you?" in processed:
        return "I am good."
    
    return "I do not understand this"
    
    
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f"User ({update.message.chat.id}) in {message_type}: {text}")
    
    if message_type == "group":
        
        if bot_name in text:
            new_text: str = text.replace(bot_name, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        return
        
    print("Bot", response)
    await update.message.reply_text(response)       
    
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}")
    
    
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(bot).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    
    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    #  Poll the bot
    print("Polling...")
    app.run_polling(poll_interval=3)    
    