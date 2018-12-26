# Import library
from __future__ import unicode_literals
from datetime import datetime
import argparse
import json
# import requests
import logging
import youtube_dl


# Variables
logging.basicConfig(filename='/tmp/getwebcontents_errors.txt', level=logging.DEBUG)
STORAGE_DIR = '/tmp/my_audio'
options = {}

'''
=> options <=
    YouTube-dl options when download audio file. It contains the configuration of how
    YouTube-dl handle data, file location, log handler,... You may want to take a look
    at Youtube-dl options pages for more information about how to configuration it.
    
    # More options can be found in:
        https://github.com/rg3/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
'''


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
                        default=STORAGE_DIR,
                        nargs='?',
                        help='Path to store audio file'
                        )
    return parser.parse_args()


# def create_connection(url):
#     return requests.get(url)


# def parse_html_content(response):
#     return response.text


# def store_download_file(data, file=''):
#     try:
#         f = open(file, 'w')
#         if type(data) == dict:
#             json.dumps(data, file)
#         else:
#             f.write(data)
#         f.close()
#         logging.info('{0} - Store data completed!'.format(datetime.now()))
#     except Exception as e:
#         logging.error('{0} - Encountered error: {1}'.format(datetime.now(), e))


def load_config(**kwargs):
    global options
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '/tmp/my_audio/%(title)s.%(ext)s',
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


def download_video(url):
    print('\n\n')
    with youtube_dl.YoutubeDL(options) as ydl:
        if type(url) == str:
            ydl.download([url])
        else:
            for element in url:
                ydl.download([element])


def main():
    # print(parse_html_content(create_connection('https://www.googleapis.com/youtube/v3/search')))
    args = parse_destination_url()
    path = ''
    if args.config:
        path = args.config
    load_config(path=path)
    # if options is None:
    #     logging.error('{0} - Encountered error: Option file not existed!'.format(datetime.now()))
    #     return 0

    if args.url is not None:
        download_video(args.url)
    else:
        print('{0:^50}'.format('Easy YouTube Downloader'))
        url = input(">>> Enter the URL of the video: ")
        download_video(url)

    print('\b\r\r[DONE]')


if __name__ == "__main__":
    main()
