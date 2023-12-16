import os
import argparse
import logging
import threading
import subprocess
import pandas as pd
from Crawler import Crawler 

class CrawlerManager:
    def __init__(self, args: argparse.Namespace, logger: logging.Logger):
        # self.output_file = args.output
        self.source = args.source
        self.cols_to_crawl = args.target # always a list
        self.cwd = os.getcwd() + "/crawler"
        self.data = pd.DataFrame()

        self.logger = logger
        self.workers = int(args.workers) if args.workers is not None else 1
        self.crawlers = []

    def download_and_unzip_source(self):
        try: 
            # download amd unzip the data from kaggle to crawl

            #commands 
            download_command = f"kaggle datasets download -d {self.source} -p {self.cwd}"
            unzip_command = f"unzip {self.cwd}/archive.zip -d {self.cwd}"

            # download 
            self.logger.info(f"downloading {self.source}")
            subprocess.run(download_command, shell=True)
            self.logger.info(f"downloaded {self.source} successfully")

            # unzip
            self.logger.info(f"unzipping archive")
            subprocess.run(unzip_command, shell=True)
            self.logger.info(f"unzipped archive successfully")
            os.remove(self.cwd + "/archive.zip")

            # finding the csv file and read it to dataframe
            self.logger.info(f"reading data...")
            for root, dirs, files in os.walk(self.cwd):
                for file in files:
                    if file.endswith(".csv"):
                        self.logger.info(f"found {file}")
                        # read the csv file to dataframe in chunks
                        for chunk in pd.read_csv(os.path.join(root, file), chunksize=1000, lines=True):
                            self.logger.info(f'READ {chunk}')
                            self.data = pd.concat([self.data, chunk])

                        self.logger.info(f"read {file} successfully")
                        break

            # check if the target column exists
            if self.col_to_crawl not in self.data.columns:
                self.logger.error(f"target column {self.col_to_crawl} does not exist")
                raise Exception(f"target column {self.col_to_crawl} does not exist")
            
            self.logger.info("Crawler initialized")

        except Exception as e:
            self.logger.error(f"Error while pre-processing source: {e}")
            raise e

    def start_workers(self):

        # self.download_and_unzip_source()

        self.logger.info(f'Starting {self.workers} crawler worker(s)')

        for _ in range(self.workers):
            crawler = Crawler(self.data, self.cols_to_crawl, self.logger) #self.output_file
            thread = threading.Thread(target=crawler.run)
            thread.start()
            self.crawlers.append(crawler)
