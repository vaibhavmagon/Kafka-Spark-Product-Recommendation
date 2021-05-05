# Command: kafka-console-consumer --bootstrap-server localhost:9092 --topic prodRecommSend --from-beginning

from kafka import KafkaConsumer
from json import loads
import json

# Consumed from Spark Stream -> Topic: prodRecommSend
consumer = KafkaConsumer(
    'prodRecommSend',
     bootstrap_servers=['localhost:9092'], # kafka Servers
     auto_offset_reset='latest', # Sends only the latest message.
     enable_auto_commit=True,
     group_id='product-recommendation', # Every consumer has to be a part of group.
     auto_commit_interval_ms=1000)

for msg in consumer:
    data = json.dumps((msg.value).decode(), indent=4, sort_keys=True)
    print('Consumer Values: ', data)