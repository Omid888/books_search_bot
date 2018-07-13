import re
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
import logging

updater = Updater('This key should be provided from telegram bot father')

logging.basicConfig(level=logging.INFO)


def find(bot, update, args):
    chat_id = update.message.chat_id
    if not args:
        bot.sendMessage(chat_id, 'هیچ کلمه ای وارد نکرده اید، برای شروع کلمه ای وارد کنید')
        return 0
    bot.sendChatAction(chat_id, "TYPING")
    a = []
    for element in args:
        try:
            a.append(dictionary[element.lower()])
        except KeyError:
            pass
    try:
        intersected = set(a[0]).intersection(*a)
        if intersected:
            for element in intersected:
                bot.sendMessage(chat_id, element)
        else:
            bot.sendMessage(chat_id, 'نتیجه ای یافت نشد')
    except IndexError:
        bot.sendMessage(chat_id, 'نتیجه ای یافت نشد')


def add(bot, update, args):
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, "TYPING")
    if args[0] not in channel_list:
        channel_list.append(args[0])
        try:
            response_add = client.invoke(ResolveUsernameRequest(args[0]))
            messages_add = client.get_messages(response_add.peer, limit=3000)
            for message in messages_add:
                this_url = 't.me/' + args[0] + '/' + str(message.id)
                try:
                    splitted = re.split(r"[\W']+", str(message.message))
                    for word in splitted:
                        if word.lower() in dictionary:
                            dictionary[word.lower()].append(this_url)
                        else:
                            dictionary[word.lower()] = this_url.split()
                except AttributeError:
                    pass
        except:
            bot.sendMessage(chat_id, 'آدرس کانال وارد شده اشتباه می باشد.لطفا نام کانال را بدون @ وارد کنید.')
        else:
            bot.sendMessage(chat_id, 'کانال درخواستی شما به ربات اضافه گردید.')
    else:
        bot.sendMessage(chat_id, 'کانال مورد نظر در مخازن ربات موجود می باشد.')


def start(bot, update):
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, "TYPING")
    key_list=[['اضافه کردن کانال','جست و جو در میان کتاب ها']]
    bot.sendMessage(chat_id,
                    "به ربات کتاب یاب خوش امدید. کتاب یاب جایی ست برای یافتن کتاب های مورد نیازتان!"
                    "برای شروع کلمه مورد نظرتان را با /find وارد کنید.\n"
                    "\nمثال:"
                    "\n/find پایگاه داده"
                    "\n/find پایگاه SQL"
                    "\n/find سیستم عامل"
                    "\n/find White Lies"
                    "\n\nیا برای اضافه کردن یک کانال به مخازن ما از مثال های زیر استفاده کنید."
                    "\n/add dl_ketab"
                    "\n/add englishbooks",reply_markup=ReplyKeyboardMarkup(key_list))


from telethon import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest

#this fields should be provided from my.telgram.com
api_id =
api_hash =

client = TelegramClient('session_name', api_id, api_hash)
client.start()
print('started')
# print(client.get_me().stringify())

dictionary = {}
channel_list = ['ebookonline', 'YarAmoozan', 'eng_books', 'bestsellers_book', 'dl_ketab', 'ketabkhanichanel']
for channel_name in channel_list:
    response = client.invoke(ResolveUsernameRequest(channel_name))
    messages = client.get_messages(response.peer, limit=3000)
    # print(messages[0].stringify())

    for message in messages:
        this_url = 't.me/' + channel_name + '/' + str(message.id)
        try:
            splitted = re.split(r"[\W']+", str(message.message))
            for word in splitted:
                if word.lower() in dictionary:
                    dictionary[word.lower()].append(this_url)
                else:
                    dictionary[word.lower()] = this_url.split()
        except AttributeError:
            pass

start_command = CommandHandler('start', start)
find_command = CommandHandler('find', find, pass_args=True)
add_command = CommandHandler('add', add, pass_args=True)
updater.dispatcher.add_handler(start_command)
updater.dispatcher.add_handler(find_command)
updater.dispatcher.add_handler(add_command)
updater.start_polling()
updater.idle()

