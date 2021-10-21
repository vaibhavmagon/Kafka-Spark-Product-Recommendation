# Kafka & Spark Streaming Product Recommendation Engine 

[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Kafka%20spark%20streaming%20product%20recommendation%20engine%20code%20on%20Python%20at&url=https://github.com/vaibhavmagon/Kafka-Spark-Product-Recommendation&via=vaibhavmagon&hashtags=python,kafka,spark,spark-streaming,developers) <img src="https://img.shields.io/static/v1?label=Python&message=3.7&color=<COLOR>"> <img src="https://img.shields.io/static/v1?label=Spark&message=2.4&color=<COLOR>"> <img src="https://img.shields.io/static/v1?label=Build&message=Passing&color=<COLOR>">

This code is to demonstrate spark streaming and kafka implementation using a real life e-commerce website product recommendation example. For any (as in data dir) specific item_id we get best recommended items.

**Disclaimer**: This is not the best tutorial for learning and implementing Recommendation engine. Though I have used item-based collaborative filtering built using python and no machine learning libraries for this tutorial.


## Data Files

- Create a /data folder with below two files.
- item-data.csv - Item Id and Item Name
```console
19444 | Radhe gold aata 25 kg
```
- user-item.csv - User Id & Item Id mapped to timestamp for matrix for collaborative filtering
```console
49721 | 19853 | 2020-09-18T20:02:20+05:30
```


## Dependencies

- Zookeeper
- Kafka
- Spark: 2.4
- Spark Stream Package: Necessary package it is part of the code.
- Python: 3.7 (for Spark 2.4 version)


## How to run?
All these commands (except for Registry of topics) go in seperate console windows on the terminal.

- **Zookeeper**: zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties <br/>
(Zoopkeeper is the broker that helps coordinate the show)

- **Kafka Server**: kafka-server-start /usr/local/etc/kafka/server.properties <br/>
(Kafka server syncs data flow between Producer and Consumers)

- **Register 1st Topic**: kafka-topics --create --zookeeper localhost:2181 --topic idpushtopic --partitions 1 --replication-factor 1 <br/>
(idpushtopic is the topic to get an Id of product for recommendations. To be run once only.)

- **Register 2nd Topic**: kafka-topics --create --zookeeper localhost:2181 --topic prodRecommSend --partitions 1 --replication-factor 1 <br/>
(prodRecommSend is the topic to which the stream pushes the recommendations. To be run once only.)

- **Producer**: kafka-console-producer --broker-list localhost:9092 --topic idpushtopic <br/>
(Producer to be opened in one window that ultimately pushes the product id to the spark stream)

- **Spark Streaming**: spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar kafka-product-recom.py localhost:2181 idpushtopic <br/>
(Stream helps fetch the Id, run the product recommendation and then acts as producer and pushes to another topic)

- **Consumer**: kafka-console-consumer --bootstrap-server localhost:9092 --topic prodRecommSend --from-beginning <br/>
(Consumer to be opened in one window that ultimately fetches the product list from the spark stream)


## How to test?

- Start Producer in one window and push an item id: 19444 (to test) <br/>

<img src="https://i.ibb.co/4wbKR14/Screenshot-2020-09-19-at-2-25-03-AM.png" alt="Screenshot-2020-09-19-at-2-25-03-AM" border="0">

- You'd see things happening on Spark streaming window. <br/>

<img src="https://i.ibb.co/Rpr4XwD/Screenshot-2020-09-19-at-2-23-38-AM.png" alt="Screenshot-2020-09-19-at-2-23-38-AM" border="0">

- Simultaneously you'd get the data in the consumer window <br/>

<img src="https://i.ibb.co/Qrck5ts/Screenshot-2020-09-19-at-2-21-15-AM.png" alt="Screenshot-2020-09-19-at-2-21-15-AM" border="0">


## Maintainer

- Vaibhav Magon
