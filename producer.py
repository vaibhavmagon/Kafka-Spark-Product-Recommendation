# Command: kafka-console-producer --broker-list localhost:9092 --topic idpushtopic

from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Producer -> Pushes to Spark Stream. Topic: idpushtopic
data = '19444'.encode()
producer.send('idpushtopic', value=data)
producer.flush() # Adding flush() before exiting will make the client wait for any outstanding messages to be delivered to the broker
print('Sent message: ', data)

# flush -> sync
# poll -> async.