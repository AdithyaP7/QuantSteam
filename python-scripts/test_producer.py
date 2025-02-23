from time import sleep
from json import dumps
from kafka import KafkaProducer

topic_name = 'my_topic123'

producer = KafkaProducer(bootstrap_servers=['localhost:9091'],value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(1000):
     data = {'number' : e}
     print(data)
     producer.send(topic_name, value=data)
     sleep(1)
     