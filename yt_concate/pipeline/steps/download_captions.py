import os
import time
import logging
from threading import Thread

from pytube import YouTube

from .step import Step
from .step import StepException
from yt_concate.settings import CAPTIONS_DIR


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(__name__)
        logger.info("in DownloadCaptions")

        start = time.time()

        threads = []
        cpu_c = os.cpu_count()
        for t in range(cpu_c):
            fun = self._ThreadDownLoadCaption(data[t::cpu_c], utils)
            threads.append(Thread(target=fun))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()

        logger.info('download all captions took', end - start, 'seconds')

        return data


    def _ThreadDownLoadCaption(self, data, utils):
        logger = logging.getLogger(__name__)

        for yt in data:

            logger.debug('downloading caption for', yt.id)
            if utils.caption_file_exist(yt):
                logger.debug('found existing caption file')
                continue
            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except AttributeError:
                logger.warning('AttributError when downloading caption for', yt.url)
                continue
            except KeyError:
                logger.warning('KeyError when downloading caption for', yt.url)
                continue

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

