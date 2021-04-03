import os
from pprint import pprint

from .step import Step
from yt_concate.settings import CAPTIONS_DIR


class ReadCaptions(Step):
    def process(self, data, inputs, utils):
        data = {}
        for captions_file in os.listdir(CAPTIONS_DIR):
            captions = {}
            with open(os.path.join(CAPTIONS_DIR, captions_file),'r') as f:
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
            data[captions_file] = captions
        pprint(data)
        return data

