from .step import Step
import logging

class ReadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(__name__)
        logger.info("in ReadCaptions")
        for yt in data:
            if not utils.caption_file_exist(yt):
                continue
            captions = {}
            with open(yt.caption_filepath,'r') as f:
                time_line = False
                time = None
                caption = None
                for line in f:
                    line = line.strip()
                    if '-->' in line:
                        time_line = True
                        time = line
                        continue
                    if time_line:
                        caption = line
                        captions[caption] = time
                        time_line = False
            yt.captions = captions
        return data

