import sys
import getopt
import logging

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.read_captions import ReadCaptions
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils


def print_usage():
    print('python -m yt_concate.main.py -c <channel_id> -s <search_word> -l <int(limit)>')
    print('python -m yt_concate.main.py'
          ' --channel_id <channel_id>'
          ' --search_word <word>'
          ' --limit <number>'
          ' --cleanup'
          ' --fast <True/False>'
          ' --log <DEBUG/INFO/WARNING/ERROR/CRITICAL>'
          )
    print("---------------------------------------------------------")
    print("OPTIONS:")
    print("{:>6} {:<12}{}".format('-c', '--channel', 'channel id of the Youtube channel to download'))
    print("{:>6} {:<12}{}".format('', '--cleanup', 'remove captions and video download during run'))


def config_logger():
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)   # 要預設到最低警告 level

    file_handler = logging.FileHandler('logging.log')  # 生成 日誌記錄輸出到文件中 的實例

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # set level
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)   # 以上設定套到 logger

    stream_handler = logging.StreamHandler()  # 生成 日誌記錄輸出到terminal中 的實例

    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def main():
    CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': "incredible",
        'limit': 20,
        'cleanup': False,
    }

    short_opts = "hc:s:l:"
    long_opts = "help channel_id= search_word= limit= cleanup".split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, args in opts:
        if opt in ['-h', '--help']:
            print_usage()
            sys.exit()
        elif opt in ['-c', '--channel_id']:
            inputs['channel_id'] = args
        elif opt in ['-s', '--search_word']:
            inputs['search_word'] = args
        elif opt == '--limit':
            inputs['limit'] = args
        elif opt == '--cleanup':
            inputs['cleanup'] = True
    if not inputs['channel_id'] or not inputs['search_word']:
        print_usage()
        sys.exit(2)
    if not str(inputs['limit']).isdigit:
        print_usage()
        sys.exit(2)

    steps = [
        Preflight(),
        GetVideoList(),   # 取得頻道所有影片id
        InitializeYT(),   # 轉為 YT model
        DownloadCaptions(),   # 下載每個影片字幕
        ReadCaptions(),   # 以字典紀錄字幕與對應時間
        Search(),   # 搜尋所有字幕含有 search_word 的片段
        DownloadVideos(),   # 下載頻道所有影片
        EditVideo(),   # 合併 Search() 所得到的片段
        Postflight(),
    ]

    config_logger()
    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()