import os
import re
import telegram
import userHelper
import requestHelper
import time
from queue import Queue

from pyngrok import ngrok
from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import *
CONTINUEBOT, HAVE, WANT, SAVECHOICE, SAVECONTACT, DROP = range(6)


def continue_with_bot(update: Update, context: CallbackContext) -> int:
    context.user_data['continueDecision'] = update.message.text
    last_message = context.user_data['continueDecision']
    if last_message == 'YES':
        update.message.reply_text(
            'You can Send /cancel to stop talking to me.')
        update.message.reply_text(
            f"Hi {update.message.from_user.first_name}! Which course do you HAVE for exchange? Enter the FIVE digit number(Third column in the class search page)")
        return HAVE

    else:
        cancel(update, context)


def start(update: Update, context: CallbackContext) -> int:
    user_data = update.message.from_user
    checkUserRequest = userHelper.checkIfUserRequestExist(user_data)
    if (checkUserRequest == False):
        userHelper.addUser(user_data)
        reply_keyboard = [['YES', 'NO']]
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing")
        update.message.reply_text('Read description before use.\n'
                                  'Enter ONE Course for each HAVE and WANT.\n'
                                  'Please enter the FIVE digit number(Third column in the class search page) for the course.\n'
                                  'You can exchange again only after your earlier exchange request is SUCCESSFUL or DROPPED.\n\n'
                                  'Will you like to continue?',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                   one_time_keyboard=True))
        return CONTINUEBOT
    else:
        print(checkUserRequest)
        replyText = f"You have already made a request on {checkUserRequest['date_created']}.You have course: <b> {checkUserRequest['have']} </b> and want course: <b>{checkUserRequest['want']}</b>, right?"
        if (checkUserRequest['status'] == 'OPEN'):
            replyText + "Your request is still open. We will notify you as soon as we hit a match"
        if (checkUserRequest['status'] == 'FOUND'):
            replyText+"We have found a match for your request. "
        if (checkUserRequest['status'] == 'COMPLETE'):
            replyText+"Your request is completed."
        update.message.reply_text(replyText, parse_mode="HTML")


def is_valid_input(input_text):
    # regular expression pattern for 5-digit number
    pattern = re.compile(r'^\d{5}$')
    return pattern.match(input_text) is not None


def have(update: Update, context: CallbackContext) -> int:
    context.user_data['have'] = update.message.text
    if not is_valid_input(context.user_data['have']):
        # handle invalid input
        update.message.reply_text("Enter only a 5 digit number!!")
        return HAVE
    # process valid input
    update.message.reply_text(
        'Which course do you WANT in exchange? Enter the FIVE digit number(Third column in the class search page)')
    return WANT


def want(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['YES', 'No, Change My Selection']]
    context.user_data['want'] = update.message.text
    if not is_valid_input(context.user_data['want']):
        # handle invalid input
        update.message.reply_text("Enter only a 5 digit number!!")
        return WANT
    # process valid input
    update.message.reply_text(
        f"{update.message.from_user.first_name}, you Have: {context.user_data['have']} and Want: {context.user_data['want']}.")
    if ({context.user_data['have']} == {context.user_data['want']}):
        update.message.reply_text(
            "You have entered the same courses for exchange. Enter again. Which course do you HAVE for exchange?")
        return HAVE
    update.message.reply_text(
        f"Will you like to continue {update.message.from_user.first_name}?\n If you contine, no further changes will be possible. Your only option will be to drop the request and raise a new one.", reply_markup=ReplyKeyboardMarkup(reply_keyboard,      one_time_keyboard=True))
    return SAVECHOICE


def saveChoice(update: Update, context: CallbackContext):
    user_data = update.message.from_user
    lastMessage = update.message.text
    if lastMessage == 'YES':
        requestId = requestHelper.addSelections(
            user_data, context.user_data['have'], context.user_data['want'])
        update.message.reply_text(
            f"Hey {update.message.from_user.first_name}! Your courses are successfully added to my database. Your Request id is: {requestId}.")
        contact_keyboard = telegram.KeyboardButton(
            text="Share Contact", request_contact=True)
        custom_keyboard = [[contact_keyboard]]
        reply_markup = telegram.ReplyKeyboardMarkup(
            custom_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Please share your contact information', reply_markup=reply_markup)
        return SAVECONTACT
    if lastMessage == 'No, Change My Selection':
        update.message.reply_text(
            f"Sure {update.message.from_user.first_name}! Which course do you HAVE for exchange?")
        return HAVE


def saveContact(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.message
    contact = message.contact
    if contact:
        userHelper.addContactNumber(
            update.message.from_user, contact.phone_number)
        message.reply_text(
            f"Thank you {user.first_name}, your contact information is {contact.phone_number}")
    else:
        message.reply_text(
            "Sorry, I was not able to get your contact information. Please try again.")
        return SAVECHOICE
    return ConversationHandler.END


def drop(update: Update, context: CallbackContext):
    user_data = update.message.from_user
    checkUserRequest = userHelper.checkIfUserRequestExist(user_data)
    if (checkUserRequest == False):
        update.message.reply_text(
            "You have no active request. Which course do you HAVE in exchange? Enter the FIVE digit number(Third column in the class search page)")
        return HAVE
    else:
        print(checkUserRequest)
        reply_keyboard = [['YES', 'NO']]
        update.message.reply_text(f"Your request made on {checkUserRequest['date_created']} for have course: <b> {checkUserRequest['have']} </b> and want course: <b>{checkUserRequest['want']}</b>, right?\n"
                                  'After you drop, you will have to create a new request and you will have to join the queue again.'
                                  'Will you like to continue?', reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                                                 one_time_keyboard=True))

    return ConversationHandler.END


def droprequest():
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END


def main() -> None:
    # http_tunnel = ngrok.connect(80, "http")
    # print("Public URL:", http_tunnel.public_url)
    print(telegram.__version__)
    application = Application.builder().token(os.environ.get('BOT_TOKEN')).build()
    bot = telegram.Bot(token=os.environ.get('BOT_TOKEN'))
    # updater = Updater(os.environ.get('BOT_TOKEN'), update_queue=Queue())
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUEBOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, continue_with_bot)],
            HAVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, have)],
            WANT: [MessageHandler(filters.TEXT & ~filters.COMMAND, want)],
            SAVECHOICE: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, saveChoice)],
            SAVECONTACT: [MessageHandler(
                filters.CONTACT & ~filters.COMMAND, saveContact)]
        },
        fallbacks=[CommandHandler('cancel', cancel),
                   CommandHandler('start', start),
                   CommandHandler('drop', drop)]
    )
    ngrok_url = ngrok.connect(5000).public_url
    print(f"Webhook URL: {ngrok_url}/webhook")
    bot.setWebhook(url=f"{ngrok_url}/{os.environ.get('BOT_TOKEN')}")
    bot.start_webhook(listen="0.0.0.0",
                      port=5000,
                      url_path="webhook",
                      webhook_url=f"{ngrok_url}/webhook")
    application.add_handler(conv_handler)
    print(bot.get_me())
    bot.set_my_status('online')
    time.sleep(300)
    bot.set_my_status('offline')
    application.run_polling()
    exit()


if __name__ == '__main__':
    main()
