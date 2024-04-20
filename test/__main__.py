from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup , Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes , CallbackQueryHandler
import asyncio
import os
import logging


TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
Webhook_url = os.environ.get('Webhook_url')
print('Starting up bot...')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)



async def start_command(update: Update, context):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')
def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text('Try typing anything, and I will do my best to respond.')

def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text('This is a custom command. You can add whatever text you want here.')


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        if query.data == '1':
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Button 2", callback_data='2'), InlineKeyboardButton("Button 3", callback_data='3')]])
            await query.edit_message_text(text=f'You selected 1',reply_markup=reply_markup)
        if query.data == '2':
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 3", callback_data='3')]])
            await query.edit_message_text(text=f'You selected 2',reply_markup=reply_markup)
        if query.data == '3':
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 2", callback_data='2')]])
            await query.edit_message_text(text=f'You selected 3',reply_markup=reply_markup)
    except Exception as e:
        print("Error while editing message : ",e)


async def echo(update: Update,context: ContextTypes.DEFAULT_TYPE):
    text = "Here are some Buttons"
    keyboard = [[InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 2", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await context.bot.send_message(chat_id=update.message.chat_id,text=text,reply_markup=reply_markup)
    except Exception as e:
        print("Error while sending message : ",e)

def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


async def setwebhhok():
    try:
        # await bot.delete_webhook()
        url_set = await bot.get_webhook_info()
        if url_set:
            await bot.set_webhook(Webhook_url + TOKEN)
        await bot.send_message(chat_id=5040666523,text=f"Bot Started !!! \n\n ``` {url_set}```",parse_mode='Markdown')
        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    bot = Bot(TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setwebhhok())

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(MessageHandler(filters.TEXT, echo))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_error_handler(error)

    print('Polling...')
    app.run_webhook(
        port=PORT,
        listen="0.0.0.0",
        # url_path= TOKEN,
        drop_pending_updates=True,
        webhook_url=Webhook_url
    )
