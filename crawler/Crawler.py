# make this script callable via cli with parameters
__author__ = "Mr_Chriwo"
__version__ = "0.0.1"
__maintainer__ = "Mr_Chriwo"
__status__ = "Development"

import os
from config import init_args
from logger import Logger
import pandas as pd
import json
from confluent_kafka import Producer
import time

class Crawler:
    def __init__(self, source: pd.DataFrame, target:list, logger: Logger): #output_file: str,
        # self.output_file = output_file
        self.logger = logger
        self.source = source
        self.target_cols = target
        self.batch_size = 255
        self.produced_batches = 0
        self.kafka_topic = "crawler"
        self.kafka_producer = Producer({'bootstrap.servers': 'knowyoursources-kafka-1:9092'})

        self.cwd = os.getcwd() + "/crawler"
        self.data = pd.DataFrame()

   
    
    def __str__(self):
        return "Crawler to crawl abstracts from the web"
    
    def crawl(self):
        self.logger.info("Crawler starts crawling - batch size: {self.batch_size}}")
        # process the batches. Each batch contains the columns of target
        for i in range(0, len(self.source), self.batch_size):
            # get the batch
            batch = self.source.iloc[i:i + self.batch_size]

            payload = batch[self.target_cols].to_dict('records')

            json_message = json.dumps(payload)

            # Produce the message to Kafka
            self.kafka_producer.produce(self.kafka_topic, key=str(self.produced_batches), value=json_message)
            print(f"Produced batch {self.produced_batches} to Kafka\r")
            time.sleep(2)

            # Wait for any outstanding messages to be delivered and delivery reports received
            self.kafka_producer.flush()
            self.produced_batches += 1    
        

        self.logger.info("Crawler finished crawling")

    def run(self):
        self.logger.info("Crawler started")
        self.crawl()
        self.logger.error("Crawler run ended")
        
        
