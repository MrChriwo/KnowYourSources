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
        self.cwd = os.getcwd()
        self.data = pd.DataFrame()

        self.logger = logger
        self.workers = int(args.workers) if args.workers is not None else 1
        self.crawlers = []

    def read_data(self, path: str, extension: str = None):
        self.logger.info(f"reading data...")
        if extension == "csv":
            for index, chunk in enumerate(pd.read_csv(path, chunksize=1000, lines=True)):
                print(f'reading chunk: {index}\r', end='', flush=True)
                self.data = pd.concat([self.data, chunk])
        elif extension == "json":
            for index, chunk in enumerate(pd.read_json(path, chunksize=1000, lines=True)):
                print(f'reading chunk: {index}\r', end='', flush=True)
                self.data = pd.concat([self.data, chunk])
        else: 
            raise Exception(f"unknown file extension {extension}")


    def check_file_extension(self, file_name: str):
        if file_name.endswith("csv"):
            self.logger.info(f"found {file_name}")
            return "csv"
        elif file_name.endswith("json"):
            self.logger.info(f"found {file_name}")
            return "json"
        else:
            return None
        
    def search_for_file(self):
        found_file = False
        for root, dirs, files in os.walk(self.cwd):
            for file in files:
                    file_extension = self.check_file_extension(file)
                    if file_extension is not None:
                        found_file = True
                        return os.path.join(root, file), file_extension
                    else:
                        continue

            if found_file:
                break

            for dir in dirs:
                dir_files = os.listdir(os.path.join(root, dir))
                for file in dir_files:
                    file_extension = self.check_file_extension(file)
                    if file_extension is not None:
                        found_file = True
                        return os.path.join(root, dir, file), file_extension
                    else:
                        continue
                break

            if found_file:
                break

    def find_zip_file(self):
        for root, dirs, files in os.walk(self.cwd):
            for file in files:
                if file.endswith("zip"):
                    return os.path.join(root, file)
                else:
                    continue     
        return None



    def download_and_unzip_source(self):

        try: 
            # download amd unzip the data from kaggle to crawl
            download_command = f"kaggle datasets download -d {self.source} -p {self.cwd}"
            self.logger.info(f"downloading {self.source}")

            subprocess.run(download_command, shell=True)
            self.logger.info(f"downloaded {self.source} successfully")

            # unzip
            self.logger.info(f"unzipping archive")
            zip_file = self.find_zip_file()

            if zip_file is not None:
                # for linux
                unzip_command = f"unzip {zip_file} -d {self.cwd}"
                subprocess.run(unzip_command, shell=True)
                self.logger.info(f"unzipped archive successfully")

                # for windows
                # unzip_command = f"Expand-Archive -Path {zip_file} -DestinationPath {self.cwd}"
                # subprocess.run(["powershell", "-Command", unzip_command], shell=True)

                # os.remove(zip_file)

                self.logger.info(f"unzipped archive successfully")

        except Exception as e:
            self.logger.error(f"Error while pre-processing source: {e}")
            raise e
    
    def check_target_columns(self):
        # check if the target column exists
        if not (col in self.data.columns for col in self.cols_to_crawl):
            self.logger.error(f"target column {self.cols_to_crawl} does not exist")
            raise Exception(f"target column {self.cols_to_crawl} does not exist")
        
    def start_workers(self):
        try:
            self.download_and_unzip_source()
            self.logger.info(f"searching data...")
            file_path, file_extension = self.search_for_file()
            self.read_data(file_path, file_extension)
            self.check_target_columns()
        except Exception as e:
            self.logger.error(f"Error while starting workers: {e}")
            raise e
        
        self.logger.info("Crawler initialized")

        
        self.logger.info(f'Starting {self.workers} crawler worker(s)')

        for _ in range(self.workers):
            crawler = Crawler(self.data, self.cols_to_crawl, self.logger) #self.output_file
            thread = threading.Thread(target=crawler.run)
            thread.start()
            self.crawlers.append(crawler)

