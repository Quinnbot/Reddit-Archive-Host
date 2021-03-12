from __future__ import unicode_literals
from datetime import datetime
import youtube_dl, sys

#YTDL.py link path

printing = False

if len(sys.argv) == 4:
    printing = True

if len(sys.argv) != 3:
    input('use: YTDL.py link path')
    exit()

link = sys.argv[1]
path = sys.argv[2]
sub = path.split('/')[2]

with open('logs/{}/{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), sub), 'a+') as f:
    f.write(f'[{datetime.now()}][downloading][{link}]--->[{path}]\n')

class Logger(object):
    def debug(self, msg):

        if printing:
            print(msg)
        pass

    def warning(self, msg):
        if printing:
            print(msg)
        pass

    def error(self, msg):

        if 'HTTP Error 404' in msg:
            with open('logs/{}/{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), sub), 'a+') as f:
                f.write(f'[{datetime.now()}][HTTP Error 404][{link}]--->[{path}]\n')
            exit(1)
        if 'No media found' in msg:
            with open('logs/{}/{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), sub), 'a+') as f:
                f.write(f'[{datetime.now()}][Error: No media found][{link}]--->[{path}]\n')
            exit()

        with open('logs/{}/{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), sub), 'a+') as f:
            f.write(f'[{datetime.now()}][{msg}][{link}]--->[{path}]\n')
        if printing:
            print(msg)

        

        


def hook(d):
    pass


ydl_opts = {
    'ignoreerrors': 'True',
    'nooverwrites': 'True',
    'outtmpl': path,
    # 'format': 'best',
    'logger': Logger(),
    'progress_hooks': [hook],
    
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])