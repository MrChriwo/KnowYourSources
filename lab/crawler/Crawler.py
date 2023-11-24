# make this script callable via cli with parameters
__author__ = "Mr_Chriwo"
__version__ = "0.0.1"
__maintainer__ = "Mr_Chriwo"
__status__ = "Development"

import argparse
from config import init_args
from logger import logger

class Crawler:
    def __init__(self, args: argparse.Namespace, logger: logger):
        self.output_file = args.output
    
        logger.info("Crawler initialized")

    def run(self):
        pass

if __name__ == '__main__':
    # get the arguments
    args = init_args()

    # check the arguments
    if not args:
        exit(1)
    
    # setup the logger
    logger = logger(args.logfile, name='[Crawler] ')

    # create the crawler
    crawler = Crawler(args, logger)

