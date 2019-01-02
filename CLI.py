# Import library
import argparse
from coreprocess import CoreProcess

"""
    This sector handle command-line interface, and inherit from CoreProcess to process data.
"""

# VARIABLES
core_process = CoreProcess()
path = ''
audio_folder = ''
format_option = 'mp3'


def parse_destination_url():
    """
    Parse all options in commandline

    :returns: url, config, file, keyword
    """
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
                        default=core_process.default_storage_directory,
                        nargs='?',
                        help='Path to store audio file'
                        )
    parser.add_argument('-F', '--format',
                        type=str,
                        default=format_option,
                        nargs='?',
                        help='Final format for the file (3gp, acc, flv, m4a, mp3, mp4, ogg, wav, webm)'
                        )
    parser.add_argument('-k', '--keyword',
                        type=str,
                        nargs='?',
                        help='Special a keyword to search in YouTube and return list of result'
                        )
    return parser.parse_args()


def user_interface():
    """
    Create a basic commandline interface and handle interact menu.
    """
    print('{:^50}'.format('Easy YouTube Downloader'))
    print('What do you want?')
    print('{0:^20}{1:^30}'.format('(1) Search from keyword', '(2) Download from link'))
    user_choose = int(input())
    if user_choose == 1:
        keyword = input('>>> Enter the keyword: ')
        print('{:^40}'.format('==> RESULT <=='))
        core_process.search_by_keywords(keyword)
    else:
        url = input('>>> Enter the URL of the video: ')
        core_process.download_video(url)
        print('\b\r\r[DONE]')


def main():
    global path, audio_folder, format_option

    args = parse_destination_url()

    if args.config is not None:
        path = args.config
    audio_folder = args.file
    format_option = args.format

    core_process.load_config(path=path, file=audio_folder, file_format=format_option)

    if args.keyword:
        core_process.search_by_keywords(args.keyword)
    elif args.url is not None:
        core_process.download_video(args.url)
        print('[DONE]')
    else:
        user_interface()


if __name__ == "__main__":
    main()
