import sys
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.context import SQLContext
from math import sqrt
from kafka import KafkaProducer

sc = SparkContext(appName="PythonStreamingKafkaProduct")
sc.setLogLevel("ERROR") # Removing INFO logs.
ssc = StreamingContext(sc, 1)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def runAlgorithm(message):
    def loadItemNames():
        itemNames = {}
        with open("data/item-data.csv") as f:
            for line in f:
                fields = line.split(",")
                itemNames[int(fields[0])] = fields[1]
        return itemNames

    # Python 3 doesn't let you pass around unpacked tuples,
    # so we explicitly extract the ratings now.
    def makePairs(userRatings):
        ratings = userRatings[1]
        (item1, rating1) = ratings[0]
        (item2, rating2) = ratings[1]
        return ((item1, item2), (rating1, rating2))

    def filterDuplicates(userRatings):
        ratings = userRatings[1]
        (item1, rating1) = ratings[0]
        (item2, rating2) = ratings[1]
        return item1 < item2

    def computeCosineSimilarity(ratingPairs):
        numPairs = 0
        sum_xx = sum_yy = sum_xy = 0
        for ratingX, ratingY in ratingPairs:
            sum_xx += ratingX * ratingX
            sum_yy += ratingY * ratingY
            sum_xy += ratingX * ratingY
            numPairs += 1

        numerator = sum_xy
        denominator = sqrt(sum_xx) * sqrt(sum_yy)

        score = 0
        if denominator:
            score = (numerator / (float(denominator)))

        return score, numPairs

    print("\nLoading product names...")
    nameDict = loadItemNames()

    data = sc.textFile("data/user-item.csv")

    # Map ratings to key / value pairs: user ID => item ID, rating
    ratings = data.map(lambda l: l.split(",")).map(lambda l: (int(l[0]), (int(l[1]), float(l[2]))))

    # Emit every item rated together by the same user.
    # Self-join to find every combination.
    joinedRatings = ratings.join(ratings)

    # At this point our RDD consists of userID => ((productId, rating), (productId, rating))

    # Filter out duplicate pairs
    uniqueJoinedRatings = joinedRatings.filter(filterDuplicates)

    # Now key by (item1, item2) pairs.
    itemPairs = uniqueJoinedRatings.map(makePairs)

    # We now have (item1, item2) => (rating1, rating2)
    # Now collect all ratings for each item pair and compute similarity
    itemPairRatings = itemPairs.groupByKey()

    # We now have (item1, item2) = > (rating1, rating2), (rating1, rating2) ...
    # Can now compute similarities.
    itemPairSimilarities = itemPairRatings.mapValues(computeCosineSimilarity).cache()

    # Extract similarities for the item we care about that are "good".
    scoreThreshold = 0.80
    coOccurenceThreshold = 20

    records = message.collect()
    responseObj = {}
    if len(records) > 0:
        productId = int(records[0]) # Here we get the productId

        # Filter for products with this sim that are "good" as defined by
        # our quality thresholds above
        filteredResults = itemPairSimilarities.filter(lambda pairSim: \
                                                           (pairSim[0][0] == productId or pairSim[0][1] == productId) \
                                                           and pairSim[1][0] > scoreThreshold and pairSim[1][
                                                               1] > coOccurenceThreshold)

        # Sort by quality score.
        results = filteredResults.map(lambda pairSim: (pairSim[1], pairSim[0])).sortByKey(ascending=False).take(10)

        if productId in nameDict:
            print("Top similar products for: " + nameDict[productId])
            for result in results:
                (sim, pair) = result
                similarProductId = pair[0]
                if similarProductId == productId:
                    similarProductId = pair[1]
                if similarProductId in nameDict:
                    print(nameDict[similarProductId] + " | " + str(similarProductId))
                    responseObj[similarProductId] = nameDict[similarProductId]
                else:
                    print('No similar products found!')

        producer.send('prodRecommSend', bytes(responseObj))
        producer.flush()


def main():
    if len(sys.argv) != 3:
        print("Usage: kafka-product-recom.py <zk> <topic>")
        exit(-1)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    #lines.pprint() # To print the status and time.
    lines.foreachRDD(runAlgorithm)

    ssc.start()
    ssc.awaitTermination()


if __name__ == '__main__':
    main()

