# Import library
from __future__ import unicode_literals
from datetime import datetime
from bs4 import BeautifulSoup
import argparse
import json
import logging
import youtube_dl
try:
    # Python 2.x
    from urllib import quote, request
except:
    # Python 3.x
    from urllib.parse import quote
    from urllib import request

'''
    This Python script enable user to download a YouTube video back to our computer and
    convert it to any format. This is a tiny project for learning new thing from Python.

                    |-----------------------------|
                    | Module used in this project |
                    |-----------------------------|

        - datetime          --> For get system time.
        - bs4/BeautifulSoup --> For working with html contents.
        - argparse          --> For enable parse arguments through CLI.
        - json              --> For working with json data.
        - logging           --> For save error information into a file for later analyse.
        - youtube-dl        --> For working with video clip in YouTube.
        - urllib            --> For working with search url.
'''
'''
    => options <=
    YouTube-dl options when download audio file. It contains the configuration of how
    YouTube-dl handle data, file location, log handler,... You may want to take a look
    at Youtube-dl options pages for more information about how to configuration it.
    
    # More options can be found in:
        https://github.com/rg3/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
'''
# Variables
logging.basicConfig(filename='./error_logs.txt', level=logging.DEBUG)
_DEFAULT_STORAGE_DIR = './my_audio/%(title)s.%(ext)s'
options = {}


class LogHandler(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
        logging.error('{0} - Error: {1}'.format(datetime.now(), msg))


def progress_handler(progress_status):
    if progress_status['status'] == 'downloading':
        print('\b\r[DOWNLOADING] {0}\tDownloaded: {1}\tTime left: {2}\tDL Speed: {3}'.format(
            progress_status['filename'],
            progress_status['downloaded_bytes'],
            progress_status['eta'],
            progress_status['speed']
        ))
    if progress_status['status'] == 'error':
        print('[ERROR] An error occupied while try to download file!')
    if progress_status['status'] == 'finished':
        print('--- Finished downloading, converting now...')


def parse_destination_url():
    parser = argparse.ArgumentParser(
        prog='python3 get-web-content.py',
        usage='%(prog)s --url=URL --config=CONFIG-FILE [OPTION]',
        description='Download YouTube video and convert it into audio format.'
    )
    parser.add_argument('-u', '--url',
                        action='append',
                        type=str,
                        nargs='?',
                        help='URL of the host'
                        )
    parser.add_argument('-c', '--config',
                        type=str,
                        nargs='?',
                        help='File contain youtube-dl options of your choose'
                        )
    parser.add_argument('-f', '--file',
                        type=str,
                        default=_DEFAULT_STORAGE_DIR,
                        nargs='?',
                        help='Path to store audio file'
                        )
    parser.add_argument('-k', '--keyword',
                        type=str,
                        nargs='?',
                        help='Special a keyword to search in YouTube and return list of result'
                        )
    return parser.parse_args()


def load_config(**kwargs):
    global options
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'restrictfilenames': True,
        'logger': LogHandler(),
        'progress_hooks': [progress_handler],
    }

    if 'outtmpl' in kwargs:
        options['outtmpl'] = kwargs['outtmpl']

    if len(kwargs['path']) != 0:
        path = kwargs['path']
        with open(path) as file:
            try:
                data = json.load(file)
                if 'format' in data:
                    options['format'] = data['format']
                if 'postprocessors' in data:
                    options['postprocessors'] = []
                    options['postprocessors'].append(data['postprocessors'])
            except json.JSONDecodeError as e:
                print('[ERROR] Unable to get files data!', e)
                logging.error('{0} - Encountered error: {1}'.format(datetime.now(), e))


def search_by_keywords(keyword=''):
    query = quote(keyword)
    search_url = "https://www.youtube.com/results?search_query=" + query
    response = request.urlopen(search_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for video in soup.find_all(attrs={'class': 'yt-uix-tile-link'}):
        print('https://www.youtube.com' + video['href'])


def download_video(url):
    print('\n\n')
    with youtube_dl.YoutubeDL(options) as ydl:
        if type(url) == str:
            ydl.download([url])
        else:
            for element in url:
                ydl.download([element])


def user_interface():
    print('{:^50}'.format('Easy YouTube Downloader'))
    print('What do you want?')
    print('{0:^20}{1:^30}'.format('(1) Search from keyword', '(2) Download from link'))
    user_choose = int(input())
    if user_choose == 1:
        keyword = input('>>> Enter the keyword: ')
        print('{:^40}'.format('==> RESULT <=='))
        search_by_keywords(keyword)
    else:
        url = input('>>> Enter the URL of the video: ')
        download_video(url)


def main():
    args = parse_destination_url()

    path = ''
    audio_folder = ''
    if args.config:
        path = args.config
    if args.file:
        audio_folder = args.file

    load_config(path=path, file=audio_folder)

    if args.keyword:
        search_by_keywords(args.keyword)
    elif args.url is not None:
        download_video(args.url)
    else:
        user_interface()
    print('\b\r\r[DONE]')


if __name__ == "__main__":
    main()
