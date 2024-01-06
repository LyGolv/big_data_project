from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Créer une source de streaming à partir de Kafka
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "trending_videos") \
    .option("startingOffsets", "earliest") \
    .load()

# Convertir les valeurs binaires de Kafka en chaînes de caractères
values_df = kafka_df.selectExpr("CAST(value AS STRING)")

# Maintenant, vous pouvez configurer d'autres transformations, actions et écrire les données de sortie
query = values_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()