import logging
from telegram import Update
from telegram.ext import ApplicationBuilder
from user import commands

TOKEN = '7301437797:AAE3CAgUWq9kOamCyE2jZG8YYXjFf7komZQ'

logging.basicConfig(
    format='%(ascitime)s - %(name)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    for _,handler in commands:
        application.add_handler(handler)
        pass
    application.run_polling()
    pass