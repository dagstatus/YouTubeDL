# -*- coding: utf-8 -*-
# 160 144p mp4
# 278 144p webm
# 133 240p mp4
# 242 240p webm
# 134 360p mp4
# 243 360p webm
# 244 480p webm
# 135 480p mp4
# 247 720p webm
# 136 720p mp4
# 248 1080p webm
# 137 1080p mp4
# 17 small 3gp
# 36 small 180 3gp
# 43 medium webm
# 18 medium 360 mp4
# 22 hd720 mp4

import youtube_dl




# with youtube_dl.YoutubeDL() as ydl:
#     listing=ydl.extract_info('https://www.youtube.com/watch?v=tbjzZHuGTng',download=False)
#

# formats=listing.get('formats')
# # print(formats)
# # print(type(formats))
# for x in formats:
#     print(x.get('format_id')+" "+x.get('format_note')+" "+x.get('ext'))




def download_video (url,options,file_name):
    #22 is 720p 18 is 360p 36 is 180p(3gp)
    #ydl_opts = {'format': '134'}\
    print(url)
    print(options)
    print(file_name)
    file_ext=str(file_name)+'.%(ext)s'
    options['outtmpl']=file_ext
    ydl_opts=options
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



# download_video('https://www.youtube.com/watch?v=tbjzZHuGTng',{'format': '18'},'test')