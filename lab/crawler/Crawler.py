# make this script callable via cli with parameters
__author__ = "Mr_Chriwo"
__version__ = "0.0.1"
__maintainer__ = "Mr_Chriwo"
__status__ = "Development"

import os
from config import init_args
from logger import Logger
import pandas as pd

class Crawler:
    def __init__(self, source: pd.DataFrame, target:list, logger: Logger): #output_file: str,
        # self.output_file = output_file
        self.logger = logger
        self.source = source
        self.cols_to_crawl = target

        self.cwd = os.getcwd() + "/crawler"
        self.data = pd.DataFrame()

   
    
    def __str__(self):
        return "Crawler to crawl abstracts from the web"
    
    def crawl(self):
        self.logger.info("Crawler started crawling")
        # process each cell in the target columns and print them 
        

        self.logger.info("Crawler finished crawling")

    def run(self):
        self.logger.info("Crawler started")
        self.logger.error("Crawler run ended")
        
        
