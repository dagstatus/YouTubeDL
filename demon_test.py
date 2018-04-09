import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import config
import time
import re
import youtube_dl
import os
from threading import Thread



TOKEN = config.token  # get token from command-line
bot = telepot.Bot(TOKEN)




def potok_for_user(msg):
    #поток для каждого пользователя создаем запускаем и передаем ему сообщение для обработки сообщений!!!
    chat_id=telepot.glance(msg)
    name_thread="Thread %s" % str(chat_id)
    message_thread=MessageThread(msg)
    message_thread.start()



class MessageThread(Thread):
    def __init__(self,msg):
        Thread.__init__(self)
        self.msg=msg

    def run(self):
        content_type, chat_type, chat_id = telepot.glance(self.msg)
        if self.msg['text']== '/numb':
            try:
                f = open('users.txt', 'r')
                i = f.read()
                f.close()

            except:
                print('error reading nunbers')
            kol_users='Количество пользователей использовавших бот - '+str(i)
            bot.sendMessage(chat_id,kol_users)
        else:
            try:
                url_txt=(re.search("(?P<url>https?://[^\s]+)", str(self.msg['text'])).group("url"))
                if 'https://www.yout' == str(url_txt)[:16] or 'https://youtu' == str(url_txt)[:13] :
                    print('It is youtube url')
                    if str(url_txt)[:16]=='https://youtu.be':
                        url_txt='https://www.youtube.com/watch?v='+url_txt[len(url_txt)-11:]
                    if str(url_txt)[:20]=='https://www.youtu.be':
                        url_txt='https://www.youtube.com/watch?v='+url_txt[len(url_txt)-11:]

                    config.chat_url[chat_id]=url_txt

                    bot.sendMessage(chat_id,'Одну минуту мы проверяем доступность видео')

                    if get_info_video(url_txt)==-1:
                        bot.sendMessage(chat_id,'Вы выбрали для скачивания плейлист, в данный момент возможно скачивание только одного файла')
                    elif get_info_video(url_txt)<420:
                        select_quality(self.msg)
                        # download_video(url_txt,config.users_qualiti.get(chat_id),chat_id)
                    else:
                        bot.sendMessage(chat_id,'Изините вы выбрали слишком длинный файл(более 7 минут). Приносим свои извинения')


            except AttributeError:
                print('BAD URL')




def select_quality(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='720p', callback_data='22')],[InlineKeyboardButton(text='360p', callback_data='18')],[InlineKeyboardButton(text='180p', callback_data='36')],
               ])

    bot.sendMessage(chat_id, 'Выберите качество', reply_markup=keyboard)

    # get_dictmsg=getmessage.get('message_id')





def on_callback_query(msg):

    query_id, chat_id, quality = telepot.glance(msg, flavor='callback_query')

    if config.user_flag.get(chat_id)==None:
        config.user_flag.update({chat_id: 0})

    if config.user_flag.get(chat_id)!=0:
        bot.answerCallbackQuery(query_id, text='Дождитесь пока предыдущий файл скачается')

    else:
        bot.answerCallbackQuery(query_id, text='Ожидайте скачивания файла')
        config.users_qualiti[chat_id]=quality
        name_thread="Thread dwld %s" % str(chat_id)
        message_thread=DownloadThread(config.chat_url.get(chat_id), str(quality), chat_id)
        message_thread.start()
        # download_video(config.chat_url.get(chat_id), str(quality), chat_id)
        config.user_flag.update({chat_id: 1})





def get_info_video (url):
    try:
        with youtube_dl.YoutubeDL() as ydl:
            listing=ydl.extract_info(url,download=False)


            # print('duration')
            # print(listing.get('duration'))

            if listing.get('_type')=='playlist':
                return (-1)
            #print(listing)
            return int(listing.get('duration'))
    except:
        print('error get duration except')

class DownloadThread(Thread):
    def __init__(self,url,options,chat_id):
        Thread.__init__(self)
        self.url=url
        self.options=options
        self.chat_id=chat_id

    def run(self):
        opt={}
        opt['format'] = str(self.options)

        print(opt)
        print(self.url)

        file_ext = str(self.chat_id) + '.%(ext)s'
        opt['outtmpl'] = file_ext

        ydl_opts=opt
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except:
            print('except dowloading')
        send_f_ext = 'mp4'
        if self.options == '36':
            send_f_ext = '3gp'

        send_f_name = str(self.chat_id) + "." + send_f_ext
        print('Sending file',str(opt))
        if self.options==22:
            print('720p')
            try:
                print('Sending at document')
                bot.sendDocument(self.chat_id,open(send_f_name,'rb'))
            except:
                print('error sending at documet')
        else:
            try:
                bot.sendVideo(self.chat_id,open(send_f_name,'rb'))
                print('sent complite, delete file')
            except:
                print('error sending file')

        try:
            config.user_flag.update({self.chat_id:0})
            #update FLAG
            print('Try delete file')
            os.remove(send_f_name)
            print('delete file complite')
        except:
            print('error delite file')

        try:
            f = open('users.txt', 'r')
            i = f.read()
            f.close()
            user_num = int(i)
        except:
            print('error reading nunbers')
        try:
            f = open('users.txt', 'w')
            f.write(str(user_num+1))
            f.close()
        except:
            print('err wr numb user')



        bot.sendMessage(self.chat_id, 'Благодарим за использование нашего бота')




MessageLoop(bot, {'chat': potok_for_user, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)
