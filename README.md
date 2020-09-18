# Kafka Spark Product Recommendation

Python script with spark streaming to get product Id from one kafka producer, find relevant products via spark streaming and publish to another topic (kafka consumer).


## Data Files (Random data for the script)

- item-data.csv - Has Item Id and Name (~3,500 entries)
- user-item.csv - User:Item Id mapped on timestamp for matrix for collaborative filtering (~10,000 entries)


## Dependencies

- Zookeeper
- Kafka
- Spark: Will be using spark streaming so dependencies accordingly.
- Python: 3.7 (for Spark 2.4 version)


## How to run?

- **Zookeeper**: zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

- **Kafka Server**: kafka-server-start /usr/local/etc/kafka/server.properties

- **Register 1st Topic**: kafka-topics --create --zookeeper localhost:2181 --topic wordcounttopic --partitions 1 --replication-factor 1

- **Register 2nd Topic**: kafka-topics --create --zookeeper localhost:2181 --topic prodRecommSend --partitions 1 --replication-factor 1

- **Producer**: kafka-console-producer --broker-list localhost:9092 --topic wordcounttopic

- **Spark Streaming**: spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar kafka-product-recom.py localhost:2181 wordcounttopic

- **Consumer**: kafka-console-consumer --bootstrap-server localhost:9092 --topic prodRecommSend --from-beginning
