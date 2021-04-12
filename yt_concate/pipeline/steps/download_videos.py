import time
import concurrent.futures
import logging

from .step import Step
from yt_concate.settings import VIDEOS_DIR

from pytube import YouTube


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(__name__)
        logger.info("in DownloadVideos")

        start = time.time()

        yt_set = set([found.yt for found in data])
        logger.debug('videos to download=', len(yt_set))
        yt_list = []

        for yt in yt_set:
            url = yt.url
            if utils.video_file_exist(yt):
                logger.debug(f'found existing video file for {url}, skipping')
                continue
            yt_list.append(yt)

        for yt in yt_list:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                executor.submit(self._DownloadVideo, yt)

        end = time.time()

        logger.info('download all videos took', end - start, 'seconds')
        return data

    def _DownloadVideo(self, yt):
        logger = logging.getLogger(__name__)
        logger.debug('downloading', yt.url)
        try:
            YouTube(yt.url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
        except:
            logger.warning(f'**** downloading {yt.url} get error ****')

