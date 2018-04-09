# -*- coding: utf-8 -*-
#Добавил проверку УРЛ
import sys
import os
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import config
import re
import DWNL

global_url=''

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='720p', callback_data='22')],[InlineKeyboardButton(text='360p', callback_data='18')],[InlineKeyboardButton(text='180p', callback_data='36')],
               ])

    bot.sendMessage(chat_id, 'Выберите качество', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Ожидайте скачивания файла')
    save_vidos(config.chat_url.get(from_id),query_data,from_id)

TOKEN = config.token  # get token from command-line

bot = telepot.Bot(TOKEN)

# bot.sendMessage(233458003,'TEST')
#bot.sendVideo(233458003,open('test.mp4', 'rb'))

# MessageLoop(bot, {'chat': on_chat_message,
#                   'callback_query': on_callback_query}).run_as_thread()

def save_vidos(url,option,fl_name):
    qualiti={}

    send_f_ext='mp4'
    if option=='36':
        send_f_ext='3gp'
    send_f_name = str(fl_name)+"."+send_f_ext
    qualiti['format']=str(option)
    bot.sendMessage(fl_name, 'Файл скачивается, пожалуйста подождите...')
    DWNL.download_video(url,qualiti,fl_name)
    print('sent video')

    bot.sendVideo(fl_name,open(send_f_name,'rb'))
    print('sent complite, delete file')
    os.remove(send_f_name)
    print('delete file complite')
    user_num=config.numbers_user
    config.numbers_user=user_num+1
    bot.sendMessage(fl_name, 'Благодарим за использование нашего бота')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if msg['text']== '/numb':
        kol_users='Количество пользователей использовавших бот - '+str(config.numbers_user)
        bot.sendMessage(chat_id,kol_users)
    else:
        try:
            url_txt=(re.search("(?P<url>https?://[^\s]+)", str(msg['text'])).group("url"))
            if 'https://www.yout' == str(url_txt)[:16] or 'https://youtu' == str(url_txt)[:13] :
                print('It is youtube url')
                if str(url_txt)[:16]=='https://www.youtu.be':
                    url_txt='https://www.youtube.com/watch?v='+url_txt[len(url_txt-11):]
                config.chat_url[chat_id]=url_txt
                bot.sendMessage(chat_id,'Одну минуту мы проверяем доступность видео')
                try:
                    if DWNL.get_info_video(url_txt)<600:
                        on_chat_message(msg)
                    else:
                        bot.sendMessage(chat_id,'Изините вы выбрали слишком длинный файл(более 10 минут). Приносим свои извинения')
                except:
                    print('error get duration in telega')
                    bot.sendMessage(chat_id,'Возникла ошибка, возможно ссылка неверная')

        except AttributeError:
            print('BAD URL')






MessageLoop(bot, {'chat':handle,'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)