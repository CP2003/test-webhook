import os
TOKEN = '6701670509:AAFcZOWlMA7VryijlHMNIT_rEYGgd3IOf-I'
PORT = 8443

import logging
import asyncio
from flask import Flask , request
from telegram import Bot , Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import Application , Updater , CommandHandler , MessageHandler , filters , ContextTypes , CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

""" 
b'{"update_id":407792343,\n"message":{"message_id":7921,"from":{"id":5040666523,"is_bot":false,"first_name":"Pamod [\\u2067[\\u26a1","username":"pamod_madubashana","language_code":"en"},"chat":{"id":5040666523,"first_name":"Pamod [\\u2067[\\u26a1","username":"pamod_madubashana","type":"private"},"date":1713520738,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}'
"""

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


@app.route('/', methods=['GET','POST'])
async def test():
    return "Hello world"

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
        webhookres = await bot.set_webhook('https://testwebhook-46698bc2b28d.herokuapp.com/' + TOKEN)
        await bot.send_message(chat_id=5040666523,text=webhookres)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    bot = Bot(TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setwebhhok())
    dp = Updater(bot,None)
    application = Application.builder().token(TOKEN).build()


    application.add_handler(MessageHandler(filters.TEXT, echo))
    application.add_handler(CallbackQueryHandler(handle_buttons))
    
    app.run(port=PORT)
