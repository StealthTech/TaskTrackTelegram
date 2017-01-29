import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater  # , Job

from datetime import datetime

from markdown import Markdown
from conversion import Convert
from deploy import Deployer


def cmd_echo_text(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def cmd_start(bot, update):
    md_user.dump('Command \'start\' invoked by chat [{chat_id}]'.format(chat_id=update.message.chat_id))

    # Rewrite: Loading proper locale id from database here
    user_language_id = 'Russian'
    user_language = languages.get(user_language_id)

    md_user.dump('Using \'{user_language_id}\' localization preset'
                 ' for user [{chat_id}]'.format(user_language_id=user_language_id, chat_id=update.message.chat_id))

    bot_response = user_language.roll_bot_response('Hello')
    user_responses = user_language.get_user_responses('Hello')

    if user_responses is not None:
        buttons = []
        for response in user_responses:
            buttons.append([KeyboardButton(user_responses.get(response))])
        kbd_hello = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        bot.sendMessage(chat_id=update.message.chat_id, text=bot_response, reply_markup=kbd_hello)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=bot_response)


def cmd_ping(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Pong!')


def telegram_cmd_init_handlers(upd):
    dispatcher = upd.dispatcher

    echo_text_handler = MessageHandler(Filters.text, cmd_echo_text)
    dispatcher.add_handler(echo_text_handler)

    dev_handler = CommandHandler('ping', cmd_ping)
    dispatcher.add_handler(dev_handler)

    start_handler = CommandHandler('start', cmd_start)
    dispatcher.add_handler(start_handler)

if __name__ == '__main__':
    # Application deployment
    start_time = datetime.now()
    deployer = Deployer()
    md_system = Markdown(deployer.PATH.get('Logs').get('System'),
                         'System ' + Convert.Date.raw_datetime(start_time, time_sep='-'))
    md_user = Markdown(deployer.PATH.get('Logs').get('Interactions'),
                       'Interactions ' + Convert.Date.raw_datetime(start_time, time_sep='-'))

    deployer.set_markdown(md_system)
    md_system.dump('Execution started at {}'.format(Convert.Date.raw_datetime(start_time)))
    deployer.deploy()
    languages = deployer.load_locales()
    try:
        # Getting access token for Telegram API
        updater = None
        try:
            token = deployer.pull('access.ini', 'Access', 'TelegramToken')
            updater = Updater(token=token)
        except (telegram.error.InvalidToken, ValueError):
            error_message = 'Error: Invalid Token passed. ' \
                            'Try to check access' \
                            ' configuration file in folder \'{}\''.format(deployer.PATH.get('Settings').get('Root'))
            md_system.dump(error_message)
            exit()

        # Starting long polling
        telegram_cmd_init_handlers(updater)
        updater.start_polling()

        # Switching to terminal mode
        console_input = ''
        while console_input.casefold() != 'stop':
            console_input = input('> ')
            if console_input == 'dev':
                pass
        updater.stop()
        raise SystemExit()

    except SystemExit:
        end_time = datetime.now()
        md_system.dump('Execution ended at {}'.format(Convert.Date.raw_datetime(end_time)))
        md_system.dump('Total uptime: {}'.format(end_time - start_time))
