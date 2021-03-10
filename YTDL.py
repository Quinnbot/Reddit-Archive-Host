from __future__ import unicode_literals
import youtube_dl, sys, datetime

#YTDL.py link path

if len(sys.argv) != 3:
    input('use: YTDL.py link path')
    exit()

link = sys.argv[1]
path = sys.argv[2]

with open('log.txt', 'a+') as f:
    f.write(f'[{datetime.datetime.now()}][downloading][{link}]--->[{path}]\n')

class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        with open('log.txt', 'a+') as f:
            f.write(f'[{datetime.datetime.now()}][{msg}][{link}]--->[{path}]\n')


def hook(d):
    pass


ydl_opts = {
    'ignoreerrors': 'True',
    'nooverwrites': 'True',
    'outtmpl': path,
    'format': 'best',
    'logger': Logger(),
    'progress_hooks': [hook],
    
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])