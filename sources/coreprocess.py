from __future__ import unicode_literals
from datetime import datetime
from urllib.parse import quote
from urllib import request
from urllib3.exceptions import HTTPError
from bs4 import BeautifulSoup
import logging
import json
import youtube_dl
import subprocess
import time
import platform

from lib.observable import notify_observers

'''
    This Python script enable user to download a YouTube video back to our computer and
    convert it to any format. This is a tiny project for learning new thing from Python.

                    |------------------------------|
                    |  Module used in this script  |
                    |------------------------------|

        - datetime          --> For get system time.
        - bs4/BeautifulSoup --> For working with html contents.
        - argparse          --> For enable parse arguments through CLI.
        - json              --> For working with json data.
        - logging           --> For save error information into a file for later analyse.
        - youtube-dl        --> For working with video clip in YouTube.
        - urllib            --> For working with search url.
        - subprocess        --> For working with shell command.
        - platform          --> For working in cross platform.
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
    """LogHandler handle messages for each case"""

    @staticmethod
    def debug(msg):
        notify_observers(msg, mode="debug")

    @staticmethod
    def warning(msg):
        notify_observers(msg, mode="warning")

    @staticmethod
    def error(msg):
        notify_observers(msg, mode="error")
        logging.error('{0} - {1}'.format(datetime.now(), msg))


def progress_handler(progress_status):
    """Handler download status"""
    notify_observers(progress_status, mode="update")
    time.sleep(0.2)


class CoreProcess(object):
    logging.basicConfig(filename='../option_and_log/error_logs.txt', level=logging.DEBUG)
    default_storage_directory = "../my_audio/%(title)s.%(ext)s"
    options_file_path = "../option_and_log/option_config.txt"
    options = {}
    status = {}

    """Main process, handleamost everything."""

    def __init__(self, options=None, storage_directory=''):
        if storage_directory is True:
            self.default_storage_directory = storage_directory
        if options is not None:
            self.options = options
        else:
            self.options = {
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': self.default_storage_directory,
                'restrictfilenames': True,
                'debug_printtraffic': False,
                'logger': LogHandler(),
                'progress_hooks': [progress_handler],
            }
        self.load_config(path=self.options_file_path)

    def load_config(self, **kwargs):
        """
        Load config from file.

        :param kwargs: Pair of keyword to indicate option (path, file,...)
        """
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
                        self.options['postprocessors'].clear()
                        self.options['postprocessors'] = data['postprocessors']
                    if 'restrictfilenames' in data:
                        self.options['restrictfilenames'] = data['restrictfilenames']
                except json.JSONDecodeError as e:
                    logging.error('{0} - {1}'.format(datetime.now(), e))

    def save_setting(self):
        """Save configuration setting to a json file"""
        data = {}
        for k, v in self.options.items():
            if isinstance(v, LogHandler):
                continue
            if type(v) == list and callable(v[0]):
                continue
            data[k] = v
        with open(self.options_file_path, "w") as file:
            try:
                json.dump(data, file)
            except TypeError as e:
                logging.error("{0} - {1}".format(datetime.now(), e))

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
            yield "https://www.youtube.com" + video['href']

    def download_video(self, url):
        """
        Download video back to local computer and convert back to format set in options.

        :param url: List of string or an string of YouTube URL want to download
        """
        try:
            with youtube_dl.YoutubeDL(self.options) as ydl:
                if type(url) == str:
                    ydl.download([url])
                else:
                    for element in url:
                        ydl.download([element])
        except HTTPError as e:
            logging.error("{0} - {1}".format(datetime.now(), e))

    def open_storage_file(self):
        """
        Open a files manager with an absolute path.

        :return: True and open Files Manager with specific path or False if file doesn't exist or wrong path.
        """
        path = self.get_absolute_path(self.options['outtmpl'])
        try:
            if platform.system() == "Linux":
                subprocess.call("nautilus -w " + path, stderr=subprocess.DEVNULL, shell=True)
            if platform.system() == "Windows":
                subprocess.call("start " + path, stderr=subprocess.DEVNULL, shell=True)
            return True
        except OSError as e:
            logging.error("{0} - {1}".format(datetime.now(), e))
            return False

    @staticmethod
    def get_absolute_path(path):
        """Get the absolute path from a relative path or a template path"""
        relate_path = False
        if path.startswith(".") or path.startswith(".."):
            relate_path = True
        temp_path = path.split("/")
        path = ""
        for i in range(len(temp_path) - 1):
            if temp_path[i] == "." or temp_path[i] == ".." or temp_path[i] == "":
                continue
            path += "/" + temp_path[i]
        if relate_path is True:
            path = subprocess.check_output("pwd").decode("utf-8").replace("\n", "") + path
        return path
