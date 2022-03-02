token = str(os.environ['TOKEN'])

import logging
from telegram import *
from telegram.ext import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = Bot(token=token)

def start(update : Update , context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    bot.send_message(ch_id , 'البوت تحت الصيانة')


def main() -> None:
    updater = Updater(token,use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters._All, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()