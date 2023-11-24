# make this script callable via cli with parameters
__author__ = "Mr_Chriwo"
__version__ = "0.0.1"
__maintainer__ = "Mr_Chriwo"
__status__ = "Development"

import argparse
from config import init_args
from logger import logger

class Crawler:
    def __init__(self, outpu_file: str, logger: logger):
        self.output_file = outpu_file
        logger.info("Crawler initialized")
    
    def __str__(self):
        return "Crawler to crawl abstracts from the web"
    
    def run(self):
        print("Crawler started")
        print("Crawler finished")
        
        
