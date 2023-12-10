import re
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# pip install python-telegram-bot

# Constants
TOKEN: Final[str] = '6789926801:AAF5hjzQScwqNoOtlJHAZKHZF_zijDz2Gz0'
BOT_USERNAME: Final[str] = '@googledrive_link_generator_bot'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! Nice to meet you. Let\'s chat!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Just type something and I will respond to you!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command.')


# Create your own response logic
def handle_response(text: str) -> str:
    file_id = re.findall("[\w\\-]{33}", text)
    url=f"https://www.googleapis.com/drive/v3/files/{file_id[0]}?alt=media&key=AIzaSyDhDSdcybHOJ032DcNhlPngZwwdw73D7NY"
    return url

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Log users
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Handle message type
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    # Reply
    print('Bot:', response)
    await update.message.reply_text(response)


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')


def main():
    print('Starting up bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Define a poll interval
    print('Polling...')
    app.run_polling(poll_interval=5)


if __name__ == '__main__':
    main()