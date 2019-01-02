from __future__ import unicode_literals
from datetime import datetime
from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup
import logging
import json
import youtube_dl

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


class LogHandler(object):
    """
    LogHandler handle messages for each case
    """
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
        logging.error('{0} - Error: {1}'.format(datetime.now(), msg))


def progress_handler(progress_status):
    """
    Here we can make anything we want referent for each process
    """
    if progress_status['status'] == 'downloading':
        print('[DOWNLOADING] {0}Downloaded: {1}Time left: {2}DL Speed: {3}'.format(
            progress_status['filename'],
            progress_status['downloaded_bytes'],
            progress_status['eta'],
            progress_status['speed']
        ))
    if progress_status['status'] == 'error':
        print('[ERROR] An error occupied while try to download file!')
    if progress_status['status'] == 'finished':
        print('--- Finished downloading, converting now...')


class CoreProcess:
    logging.basicConfig(filename='./error_logs.txt', level=logging.DEBUG)
    default_storage_directory = './my_audio/%(TITLE)s.%(EXT)s'
    options = {}

    """
    Main process, handle amost everything.
    """

    def __init__(self, options=None, default_storage_directory=''):
        if options is not None:
            self.options = options
        if default_storage_directory is True:
            self.default_storage_directory = default_storage_directory

    def load_config(self, **kwargs):
        """
        Load config from file.

        :param kwargs: Pair of keyword to indicate option (path, file,...)
        """
        self.options = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'restrictfilenames': True,
            'logger': LogHandler(),
            'progress_hooks': [progress_handler],
        }

        if 'file' in kwargs:
            self.options['outtmpl'] = kwargs['file']
        if 'file_format' in kwargs:
            self.options['postprocessors'][0]['preferredcodec'] = kwargs['file_format']

        if len(kwargs['path']) != 0:
            path = kwargs['path']
            with open(path) as file:
                try:
                    data = json.load(file)
                    if 'format' in data:
                        self.options['format'] = data['format']
                    if 'postprocessors' in data:
                        self.options['postprocessors'] = []
                        self.options['postprocessors'].append(data['postprocessors'])
                except json.JSONDecodeError as e:
                    logging.error('{0} - Encountered error: {1}'.format(datetime.now(), e))

    @staticmethod
    def search_by_keywords(keyword=''):
        """
        Send search request to YouTube with keyword and show result.

        :param str keyword: Keyword to search on YouTube
        """
        query = quote(keyword)
        search_url = "https://www.youtube.com/results?search_query=" + query
        response = request.urlopen(search_url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        for video in soup.find_all(attrs={'class': 'yt-uix-tile-link'}):
            print('https://www.youtube.com' + video['href'])

    def download_video(self, url):
        """
        Download video back to local computer and convert back to format set in options.

        :param url: List of string or an string of YouTube URL want to download
        """
        with youtube_dl.YoutubeDL(self.options) as ydl:
            if type(url) == str:
                ydl.download([url])
            else:
                for element in url:
                    ydl.download([element])