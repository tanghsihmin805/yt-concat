from .step import Step
import logging


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(__name__)
        logger.info("in Postflight")
        pass
