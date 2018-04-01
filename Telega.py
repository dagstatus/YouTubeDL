# -*- coding: utf-8 -*-
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import config

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='720p', callback_data='22')],[InlineKeyboardButton(text='360p', callback_data='18')],[InlineKeyboardButton(text='180p', callback_data='36')],
               ])

    bot.sendMessage(chat_id, 'Выберите качество', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')

TOKEN = config.token  # get token from command-line

bot = telepot.Bot(TOKEN)

# bot.sendMessage(233458003,'TEST')
#bot.sendVideo(233458003,open('test.mp4', 'rb'))

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)