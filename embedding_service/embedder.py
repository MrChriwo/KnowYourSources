from confluent_kafka import Consumer, KafkaError, Producer
import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, CollectionsResponse
import argparse
from transformers import AutoTokenizer, AutoModel
import requests
import threading
import os

# ============================= GET ARGS =============================#
parser = argparse.ArgumentParser()
parser.add_argument('--collection', type=str, help='Qdrant Collection name', required=True)

args = parser.parse_args()

# ====================================================================#


# ============================= EMBEDDING MODEL =============================#

tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
model = AutoModel.from_pretrained('allenai/specter')

# ===========================================================================#


# ============================= KAFKA CONFIG =============================#
conf1 = {
    'bootstrap.servers': 'knowyoursources-kafka-1',
    'group.id': 'embedding-service',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
}

user_request_conf = {
    'bootstrap.servers': 'knowyoursources-kafka-2',
    'enable.auto.commit': True,
    'client.id': 'embedding-service',
    'group.id': 'django-responder',
}
crawler_consumer = Consumer(conf1)
crawler_consumer.subscribe(['crawler'])

request_consumer = Consumer(user_request_conf)
request_consumer.subscribe(['request'])

response_producer = Producer(user_request_conf)

# ==========================================================================#


# ============================= QDRANT CONFIG =============================#


qdrant_host = "qdrant-vector-db"
qdrant_client = QdrantClient(host=qdrant_host)

def check_connection(collection_name):
    api_key = os.environ.get("QDRANT_API_KEY")
    host = os.environ.get("HOST")
    try:
        response = requests.get(f"http://{host}/collections/qdrant/{collection_name}", headers={
            "accept": "*",
            "api-key": api_key
        })
        response = response.json()
        if response["status"] != "ok":
            print(f"collection {collection_name} does not exist")
            return False
        print(f"collection {collection_name} found")
        return True
    except:
        return False

# check if qdrant collection exists
if not check_connection(args.collection):
    qdrant_client.recreate_collection(collection_name=args.collection, vectors_config=VectorParams(size=768, distance=Distance.COSINE))
    print(f"collection {args.collection} created")

# ==========================================================================#

processed_batch = 0
message_id = 0


def get_embedding(title, abstract):
    inputs = tokenizer(title + abstract, padding=True, truncation=True, return_tensors="pt", max_length=512)
    outputs = model(**inputs)
    return  outputs.last_hidden_state[:, 0, :].detach().numpy().flatten()


# Function to process a batch of messages
def process_batch(messages, is_crawler):
    global processed_batch
    global message_id
    print("start reading message")

    for message in messages:
        value = json.loads(message.value())

        if is_crawler:
            for struct in value:
                title = struct.get('title', '')
                authors = struct.get('authors', '')
                abstract = struct.get('abstract', '')
                category = struct.get('categories', '')
                doi = struct.get('doi', '')

                # ============================= EMBEDDING =============================#
                print("start embedding")
                embedding = get_embedding(title, abstract)

                document = {
                        'title': title,
                        'authors': authors,
                        'abstract': abstract,
                        'category': category,
                        'doi': doi,
                        }
                
                print("document title", document['title'] + " recieved")
                
                
                print("start pushing to qdrant")
                # pushing to qdrant
                try:
                    qdrant_client.upsert(
                            collection_name=args.collection,
                            points=[
                                PointStruct(
                                    id=message_id,
                                    vector=embedding.tolist(),
                                    payload=document,
                                )
                            ]
                        )
                except Exception as e:
                    print("error occured while pushing to qdrant", e)
                    continue
                
                message_id += 1
                processed_batch += 1
                print(f"Processed Batch Job {processed_batch}")

    # ================= for user requests =========================#
        else: 
            response = {
                "title": value["title"],
                "embedding": get_embedding(value["title"], value["abstract"]).tolist()
            }
            response_producer.produce('request_response', json.dumps(response))
        
    #=============================================================#
            

#=============================END OF EMBEDDING ================================#




def process_from_crawler():
    while True:
        print("start consuming crawler")

        try:
            messages = crawler_consumer.consume(num_messages=2)

            if len(messages) == 0:
                print("No messages consumed")
                continue

            print(f"Consumed {len(messages)} messages")
            for message in messages:
                if message.error() is not None:
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(message.error())
                        break

            # Process the batch of messages
            process_batch(messages, True)


        except Exception as e:
            print("error occured, trying again", e)
            continue

def process_user_requests(): 
    while True:
        print("start consuming")

        try:
            messages = request_consumer.consume(num_messages=1)

            if len(messages) == 0:
                print("No messages consumed")
                continue

            print(f"Consumed {len(messages)} messages")
            for message in messages:
                if message.error() is not None:
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(message.error())
                        break
            # Process the batch of messages
            process_batch(messages, False)


        except Exception as e:
            print("error occured, trying again", e)
            continue


try:
    crawler_processing = threading.Thread(target=process_from_crawler)
    user_request_processing = threading.Thread(target=process_user_requests)

    crawler_processing.start()
    user_request_processing.start()

    crawler_processing.join()
    user_request_processing.join()

except Exception as e:
    print("error occured", e)
