# Standard Import
import logging

# Telegram Import
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

# Local Import
import ptr_utils
import ptr_report
CONFIG = ptr_utils.receive_cfg()

updater = Updater(token=CONFIG['token'])
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

############################################################################
# Commands
############################################################################

# Command: /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! :)")
    bot.send_message(chat_id=update.message.chat_id, text=ptr_utils.show_commands())
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=ptr_utils.show_commands())
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def report(bot, update, args):
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text="Incorrect argument. Format: /report num_days.")
    elif not args[0].isdigit():
        bot.send_message(chat_id=update.message.chat_id, text="Incorrect argument. Bot supports numbers only! Format: /report num_days.")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Generating {} day report...".format(int(args[0])))
        bot.send_message(chat_id=update.message.chat_id, text=ptr_report.return_logs(CONFIG, args))
report_handler = CommandHandler('report', report, pass_args=True)
dispatcher.add_handler(report_handler)

def donate(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Support development (or buy me a beer) by donating LTC here: LeVVJYFuPa5gPVtUCpz8vY2U5EGYL1zKDd")
donate_handler = CommandHandler('donate', donate)
dispatcher.add_handler(donate_handler)

# Command: /caps "input"
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)
caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

# Command: Invalid
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

############################################################################
# Messages
############################################################################

# Messages: Any non-command
def echo(bot, update):
    # bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text="Hi :)")
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

############################################################################
# Start Bot!
############################################################################
updater.start_polling()
