from django.http import HttpResponse
from confluent_kafka import Producer
from confluent_kafka import Consumer
from qdrant_client import QdrantClient
import json

# ==================== request structures ====================

request_specter_structure = ["title", "abstract"]

# ============================================================


# ==================== kafka Producer ====================
conf = {'bootstrap.servers': "knowyoursources-kafka-2:9092",
        'client.id': 'django-requestor',
        'default.topic.config': {'acks': 'all'}}

producer = Producer(conf)
# producer topic 
request_topic = "request"

# =========================================================


# ==================== kafka Consumer ====================

conf = {'bootstrap.servers': "knowyoursources-kafka-2:9092",
        'client.id': 'django-responder',
        'group.id': 'django-responder',
        'auto.offset.reset': 'earliest'}

consumer = Consumer(conf)
# consumer topic
response_topic = "request_response"
consumer.subscribe([response_topic])

# =========================================================



# ==================== Qdrant config ====================

qdrant_host = "qdrant-vector-db"
qdrant_client = QdrantClient(host=qdrant_host)

def perform_simlarity_search(embedding, collection_name: str, limit=10):
    
    hits = qdrant_client.search(
    collection_name=collection_name,
    query_vector=embedding,
    limit=limit,
    )
    
    return hits

# =========================================================

def predict(request, params):
    if request.method == "GET":
        return HttpResponse("Please send a POST request", status=400)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            if not all([key in data for key in request_specter_structure]):
                return HttpResponse("Please send a valid request", status=400)
            else:
                producer.produce(request_topic, json.dumps(data))
                producer.flush()
                found_response = False
                while not found_response:
                    msg = consumer.consume()
                    if msg is None:
                        continue
                    if msg.error():
                        print("Consumer error: {}".format(msg.error()))
                        continue
                    else:
                        values = json.loads(msg.value())
                        if values["title"] == data["title"]:
                            found_response = True
                            embedding = values["embedding"]
                            response = perform_simlarity_search(embedding, params)

                            if isinstance(response, list) and all(isinstance(item, dict) for item in response):
                                response = json.dumps(response)
                                return HttpResponse(response, status=200)
                            else:
                                return HttpResponse("Invalid response format from Qdrant", status=500)
                        return HttpResponse(response, status=200)
        except Exception as e:
            print(e)
            return HttpResponse("internal server error", status=500)
