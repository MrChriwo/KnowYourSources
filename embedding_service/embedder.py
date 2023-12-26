from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import argparse
from transformers import AutoTokenizer, AutoModel
import requests

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
conf = {
    'bootstrap.servers': 'knowyoursources-kafka-1',
    'group.id': 'embedding-service',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
}
consumer = Consumer(conf)
consumer.subscribe(['crawler'])

# ==========================================================================#


# ============================= QDRANT CONFIG =============================#

def check_connection(collection_name, host):
    try:
        response = requests.get(f"http://{host}/collections/{collection_name}")["result"]
        if response["status"] != "ok":
            print(f"collection {collection_name} does not exist")
            return False
        print(f"collection {collection_name} found")
        return True
    except:
        return False

qdrant_host = "qdrant-vector-db"
qdrant_client = QdrantClient(host=qdrant_host)

# check if qdrant collection exists
if not check_connection(args.collection, qdrant_host):
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
def process_batch(messages):
    global processed_batch
    global message_id
    print("start reading message")

    for message in messages:
        value = json.loads(message.value())

        for struct in value:
            title = struct.get('title', '')
            authors = struct.get('authors', '')
            abstract = struct.get('abstract', '')
            category = struct.get('category', '')

            # ============================= EMBEDDING =============================#
            print("start embedding")
            embedding = get_embedding(title, abstract)

            document = {
                    'title': title,
                    'authors': authors,
                    'abstract': abstract,
                    'category': category,
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
            #=======================================================================#

        processed_batch += 1
        print(f"Processed Batch Job {processed_batch}")



# Consume messages in batches
while True:
    print("start consuming")

    try:
        messages = consumer.consume(num_messages=2)

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
        process_batch(messages)


    except Exception as e:
        print("error occured, trying again", e)
        continue