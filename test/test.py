import logging
import asyncio
from flask import Flask , request
from telegram import Bot , Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import Application , Updater , CommandHandler , MessageHandler , filters , ContextTypes , CallbackQueryHandler
import os 

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
Webhook_url = os.environ.get('Webhook_url')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['GET','POST'])
async def webhook():
    try: 
        update = Update.de_json(request.get_json(), bot)
        await Application.initialize(application)
        await application.process_update(update)
        return "ok"
    except Exception as e: 
        print("Error 1",e)
        return "Fail"

async def echo(update: Update,context: ContextTypes.DEFAULT_TYPE):
    text = "Here are some Buttons"
    keyboard = [[InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 2", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await context.bot.send_message(chat_id=update.message.chat_id,text=text,reply_markup=reply_markup)
    except Exception as e:
        print("Error while sending message : ",e)


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
async def setwebhhok():
    try:
        # await bot.delete_webhook()
        await bot.set_webhook('Webhook_url' + TOKEN)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    bot = Bot(TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setwebhhok())
    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT, echo))
    application.add_handler(CallbackQueryHandler(handle_buttons))
    app.run(port=PORT)
