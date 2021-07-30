#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, datetime, pytz, os

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def wen(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.message.chat.type == "private":
        update.message.reply_text(f"{wenChris()} days until chris returns")
    elif update.message.chat.type == "group" or update.message.chat.type == "supergroup":
        if('@wenchris_bot' in update.message.text):
            update.message.reply_text(f"{wenChris()} until Chris returns",quote=False)

def wenChris():
  PST = pytz.timezone("America/Vancouver")  
  today = PST.localize(datetime.datetime.today(), is_dst=None)
  future = PST.localize(datetime.datetime(2022,1,3,9,0,0), is_dst=None)
  diff = future - today
  d = {"days": diff.days}
  d["hours"], rem = divmod(diff.seconds, 3600)
  d["minutes"], d["seconds"] = divmod(rem, 60)
  return f'{d["days"]} Days, {d["hours"]} Hours, {d["minutes"]} Minutes, {d["seconds"]} seconds'

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get("api-token"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, wen))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
