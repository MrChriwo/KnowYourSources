import argparse
import logging
import threading
from Crawler import Crawler 

class CrawlerManager:
    def __init__(self, args: argparse.Namespace, logger: logging.Logger):
        self.output_file = args.output
        self.logger = logger
        self.workers = int(args.workers) if args.workers is not None else 1
        self.crawlers = []

    def start_workers(self):
        self.logger.info(f'Starting {self.workers} crawler worker(s)')

        for _ in range(self.workers):
            crawler = Crawler(self.output_file, self.logger)
            thread = threading.Thread(target=crawler.run)
            thread.start()
            self.crawlers.append(crawler)
