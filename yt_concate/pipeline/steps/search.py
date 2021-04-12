from .step import Step
import logging
from yt_concate.model.found import Found


class Search(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(__name__)
        logger.info("in Search")
        search_word = inputs['search_word']
        qq = False
        found = []
        for yt in data:
            captions = yt.captions
            if not captions:
                continue
            for caption in captions:
                if search_word in caption:
                    time = captions[caption]
                    f = Found(yt, caption, time)
                    found.append(f)

        logger.info(f"found {inputs['search_word']} at all videos has {len(found)} times")
        return found
