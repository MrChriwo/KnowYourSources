from config import init_args
from logger import Logger
from manager import CrawlerManager

if __name__ == '__main__':
    # get the arguments
    args = init_args()

    # check the arguments
    if not args:
        exit(1)
    
    # setup the logger
    logger = Logger(args.logfile, name='Crawler')

    # create the crawler
    crawler = CrawlerManager(args, logger)
    crawler.start_workers()