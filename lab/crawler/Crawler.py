# make this script callable via cli with parameters
__author__ = "Mr_Chriwo"
__version__ = "0.0.1"
__maintainer__ = "Mr_Chriwo"
__status__ = "Development"

from config import init_args
from logger import Logger

class Crawler:
    def __init__(self, outpu_file: str, logger: Logger):
        self.output_file = outpu_file
        self.logger = logger
        self.logger.info("Crawler initialized")
    
    def __str__(self):
        return "Crawler to crawl abstracts from the web"
    
    def run(self):
        self.logger.info("Crawler started")
        self.logger.error("Crawler run ended")
        
        
