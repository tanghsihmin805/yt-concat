from .step import Step
from yt_concate.model.yt import YT
import logging


class InitializeYT(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(__name__)
        logger.info("in InitializeYT")
        return [YT(url) for url in data]