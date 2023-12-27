# make this script callable via cli with parameters
__author__ = "Mr_Chriwo"
__version__ = "1.0.0"
__maintainer__ = "Mr_Chriwo"
__status__ = "Development"

import os
from config import init_args
from logger import Logger
import pandas as pd
import json
from confluent_kafka import Producer
import time
import sqlite3

class Crawler:
    def __init__(self, target:list, logger: Logger, extension: str, path: str, kaggle_source: str): #output_file: str,
        # self.output_file = output_file
        self.path = path
        self.extension = extension
        self.logger = logger
        self.target_cols = target
        self.kaggle_source = kaggle_source

        self.batch_size = 255
        self.produced_batches = 0
        self.kafka_topic = "crawler"
        self.kafka_producer = Producer({'bootstrap.servers': 'knowyoursources-kafka-1:9092'})

        self.db_path = os.path.join(os.path.dirname(__file__), 'data', 'crawler.db')
        self.starting_chunk_index = 0
        
    
    def __str__(self):
        return "Crawler to crawl abstracts from the web"
        
    

    def init_db(self):
        self.logger.info("Initializing database...")
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute('''
                      CREATE TABLE IF NOT EXISTS current_jobs (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      chunk_index INTEGER,
                      timestamp REAL)''')
            c.execute('''
                        CREATE TABLE IF NOT EXISTS finished_jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        timestamp REAL)''')
            
            conn.commit()
            self.logger.info("Database initialized!")
            conn.close()

        except Exception as e:
            self.logger.error(f"Error while initializing database: {e}")
            raise e
        

    def check_if_job_finished(self):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute(f"SELECT name FROM finished_jobs WHERE name = '{self.kaggle_source}'")
            finished_job = c.fetchone()

            if finished_job is None:
                conn.close()
                return False
            else:
                conn.close()
                return True


        except Exception as e:
            self.logger.error(f"Error while retrieving current job from database: {e}")
            raise e

    def handle_current_job(self):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute(f"SELECT chunk_index FROM current_jobs WHERE name = '{self.kaggle_source}'")
            current_job = c.fetchone()

            if current_job is None:
                c.execute(f"INSERT INTO current_jobs (name, chunk_index, timestamp) VALUES ('{self.kaggle_source}', 0, '{time.time()}')")
                self.logger.info(f"starting from chunk 0")
                conn.commit()
            else:
                self.logger.info(f"starting from chunk {current_job[0]} | row {current_job[0] * self.batch_size}")
                self.starting_chunk_index = current_job[0] if current_job is not None else 0

            conn.close()

        except Exception as e:
            self.logger.error(f"Error while retrieving current job from database: {e}")
            raise e
        
    
    def update_current_job(self, chunk_index):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute(f"UPDATE current_jobs SET chunk_index = '{chunk_index}' WHERE name = '{self.kaggle_source}'")
            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Error while updating current job in database: {e}")
            raise e
        
    def update_finished_jobs(self):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute(f"INSERT INTO finished_jobs (name, timestamp) VALUES ('{self.kaggle_source}', '{time.time()}')")
            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Error while updating finished jobs in database: {e}")
            raise e
        
    def crawl(self):
        self.logger.info("Crawler starts crawling - batch size: {self.batch_size}}")

        try:
            self.logger.info(f"reading data...")
            if self.extension == "csv":
                for index, chunk in enumerate(pd.read_csv(self.path, chunksize=self.batch_size, lines=True, skiprows= (self.starting_chunk_index * self.batch_size))):
                    payload = chunk[self.target_cols].to_dict('records')
                    json_message = json.dumps(payload)

                    #Produce the message to Kafka
                    self.kafka_producer.produce(self.kafka_topic, key=str(self.produced_batches), value=json_message)
                    print(f"Produced batch {self.produced_batches} to Kafka\r", end='', flush=True)
                    self.update_current_job(index)
                    time.sleep(2)

                    self.kafka_producer.flush()
                    self.produced_batches += 1
                
                self.update_finished_jobs()
                self.logger.info("Crawler finished crawling")

            elif self.extension == "json":
                for index, chunk in enumerate(pd.read_json(self.path, chunksize=self.batch_size, lines=True)):

                    if index < self.starting_chunk_index:
                        continue

                    payload = chunk[self.target_cols].to_dict('records')
                    json_message = json.dumps(payload)

                    # Produce the message to Kafka
                    self.kafka_producer.produce(self.kafka_topic, key=str(self.produced_batches), value=json_message)
                    print(f"Produced batch {self.produced_batches} to Kafka\r", end='', flush=True)
                    self.update_current_job(index)
                    time.sleep(2)

                    self.kafka_producer.flush()
                    self.produced_batches += 1
                
                self.update_finished_jobs()
                self.logger.info("Crawler finished crawling")
                    
            else: 
                raise Exception(f"unknown file extension {self.extension}")
        except Exception as e:
            self.logger.error(f"Error while crawling: {e}")
            raise e

    def idle(self):
        self.logger.info("Crawler went to idling")
        while True:
            time.sleep(10)

    def run(self):
        self.logger.info("Crawler started")
        self.init_db()
        is_finished = self.check_if_job_finished()
        if is_finished:
            self.logger.info("Job is already finished")
            self.idle()
        else:
            self.handle_current_job()
            self.crawl()
            self.logger.info("Crawler run ended")
            self.idle()
        