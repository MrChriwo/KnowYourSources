from django.http import HttpResponse
from confluent_kafka import Producer, Consumer, KafkaError
from qdrant_client import QdrantClient
import json

# ==================== request structures ====================

request_specter_structure = ["title", "abstract"]

# ============================================================


# ==================== kafka Producer ====================
conf = {'bootstrap.servers': "knowyoursources-kafka-2",
        'client.id': 'django-requestor',
        'default.topic.config': {'acks': 'all'}}

producer = Producer(conf)
# producer topic 
request_topic = "request"

# =========================================================


# ==================== kafka Consumer ====================

conf = {'bootstrap.servers': "knowyoursources-kafka-2",
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
    print("hi i am the similarity search function")
    hits = qdrant_client.search(
    collection_name=collection_name,
    query_vector=embedding,
    limit=limit,
    )

    print("hits found, converting to list")
    response = []

    for hit in hits:
        payload = hit.payload
        score = hit.score
        payload["score"] = score
        response.append(payload)
        print(f"appended {payload} to response")
        
    return response

# =========================================================

def predict(request, params):
    if request.method == "GET":
        return HttpResponse("Please send a POST request", status=400)
    elif request.method == "POST":
        print("initiating request")
        try:
            data = json.loads(request.body)
            if not all([key in data for key in request_specter_structure]):
                return HttpResponse("Request body not satisfied", status=400)
            else:
                print("producing to kafka")
                producer.produce(request_topic, json.dumps(data))
                producer.flush()
                found_response = False

                while not found_response:
                    messages = consumer.consume(num_messages=1)

                    if len(messages) == 0:
                        print("No messages consumed")
                        continue

                    print(f"Consumed {len(messages)} messages")
                    for message in messages:
                        if message.error() is not None:
                            if message.error().code() == KafkaError._PARTITION_EOF:
                                return HttpResponse("Internal Server Error", status=500)

                        else:
                            print("np message error, processing message")
                            values = json.loads(message.value())
                            if values["title"] == data["title"]:
                                found_response = True
                                embedding = values["embedding"]
                                print("embedding found, performing similarity search")
                                response = perform_simlarity_search(embedding, params)
                                if isinstance(response, list) and all(isinstance(item, dict) for item in response):
                                    print("response found, returning response")
                                    response = json.dumps(response)
                                    found_response = True
                                    return HttpResponse(response, status=200)
                                else:
                                    return HttpResponse("Invalid response format from Qdrant", status=500)
                            else:
                                print("title not found, continuing")
                                continue
                                
        except Exception as e:
            print(e)
            return HttpResponse("internal server error", status=500)
        
    else:
        return HttpResponse("Method not allowed", status=405)