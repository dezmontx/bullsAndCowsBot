import random
import sqlite3

import telegram
from dbhelper import DBHelper
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram.ext.dispatcher import run_async

import config

bot = telegram.Bot(token=config.TOKEN)

updater = Updater(config.TOKEN)

dispatcher = updater.dispatcher

db = DBHelper()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=config.RULES)


@run_async
def bulls_and_cows(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=get_bulls_and_cows(chat_id=update.message.chat_id, guess_number=update.message.text))


def generate_purpose_number():
    purpose_number = ""
    for i in range(4):
        purpose_number += str(random.randint(0, 9))
    return purpose_number


game_handler = MessageHandler(Filters.text, bulls_and_cows)
dispatcher.add_handler(game_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def validate_number(number):
    if len(number) != 4:
        return False

    for digit in number:
        if not digit.isdigit():
            return False

    return True


def get_bulls_and_cows(chat_id, guess_number):
    residual_letters_from_purpose = ''
    residual_letters_from_guess = ''

    bulls = 0
    cows = 0

    if not validate_number(guess_number):
        return 'Неправильный формат ввода! Вы должны ввести четырехзначное число!'

    try:
        purpose_number = ''
        cursor = db.get_user_number(chat_id).fetchone()
        if cursor is None:
            purpose_number = generate_purpose_number()
            db.add_user_number(chat_id, purpose_number)
        else:
            purpose_number = cursor[0]
            if purpose_number == '0':
                purpose_number = generate_purpose_number()
                db.update_user_number(chat_id, purpose_number)

    except sqlite3.Error as er:
        print(er)

    i = 0
    for digit in guess_number:
        if digit == purpose_number[i]:
            residual_letters_from_purpose += "_"
            bulls += 1
        else:
            residual_letters_from_purpose += purpose_number[i]
            residual_letters_from_guess += guess_number[i]

        i += 1

    for digit in residual_letters_from_guess:
        for another_digit in residual_letters_from_purpose:
            if digit == another_digit:
                cows += 1
                residual_letters_from_purpose = residual_letters_from_purpose.replace(digit, "_", 1)
                break

    if bulls == 4:
        db.update_user_number(chat_id, '0')

    return str(bulls) + " B " + str(cows) + " K"


def main():
    db.setup()
    updater.start_polling()


if __name__ == '__main__':
    main()
