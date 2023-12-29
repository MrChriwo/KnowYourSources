import json 
from channels.generic.websocket import WebsocketConsumer


class PredictionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'prediction': 'connected'
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        self.send(text_data=json.dumps({
            'prediction': text_data_json['prediction']
        }))