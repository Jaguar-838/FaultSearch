from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import search
import tg_webApi

#pip install python-telegram-bot

# Включите ведение журнала
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def my_function():
    search.start()
    return 'ok'

def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = my_function()
    update.message.reply_text(result)

def main() -> None:
    application = ApplicationBuilder().token(tg_webApi._token).build()
    start_handler = CommandHandler('get', run)
    application.add_handler(start_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
