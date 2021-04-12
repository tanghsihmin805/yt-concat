from .step import Step
import logging


class Preflight(Step):
    def process(self, data, inputs, utils):

        logger = logging.getLogger(__name__)
        logger.info("in Preflight")
        utils.creat_dir()
        if inputs['cleanup']:
            utils.clean_dir()
