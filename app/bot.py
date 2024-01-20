import asyncio
import httpx
import os
from telegram.ext import CommandHandler, Application, MessageHandler, filters, ContextTypes
from telegram import Update
import random
from dotenv import load_dotenv
from expressions import text_to_list, text
import requests

load_dotenv()
bot = os.getenv('TOKEN')
bot_name = '@bot'

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
    text: str = update.message.text
    print(f"Received message: {text}")

    # Перевіряємо, чи повідомлення містить згадку бота
    if bot_name in text:
        # Видаляємо згадку бота з тексту
        text = text.replace(bot_name, "").strip()

        if text:
            # Обробляємо текстове повідомлення
            response = handle_response(text)
            await update.message.reply_text(response)
        else:
            # Якщо текст відсутній після видалення згадки бота
            await update.message.reply_text("Будь ласка, надішліть текстове повідомлення.")
    else:
        # Якщо повідомлення не містить згадки бота, просто повертаємо управління
        return
       
    
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}")
    
    
    


async def ask_openai(prompt, max_tokens=150):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    headers = {'Authorization': f'Bearer {openai_api_key}'}
    data = {
        'model': 'gpt-4-vision-preview',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            latest_message = response_json.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            return latest_message
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            print(f"Response body: {e.response.text}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None




    
    
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
    app.add_error_handler(lambda u, c: print(f"Error: {c.error}"))
    
    #  Poll the bot
    print("Polling...")
    app.run_polling(poll_interval=3)    
    