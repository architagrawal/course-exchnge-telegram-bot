from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
import telegram
import os
import userHelper
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext


def broadcastMessageToAll(message):
    bot = telegram.Bot(token=os.environ.get('BOT_TOKEN'))
    listOftelegramid = userHelper.fetchAllUserTelegramId()
    print("here", listOftelegramid)
    for telegramId in listOftelegramid:
        bot.send_message(chat_id=telegramId[0], text=message)


def sendMessage(message, chatId):
    bot = telegram.Bot(token=os.environ.get('BOT_TOKEN'))
    bot.send_message(chat_id=chatId, text=message)
