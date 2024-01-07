import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, ArrayType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_spark():
    return SparkSession.builder.getOrCreate()


def get_schema():
    schema = StructType([
        StructField("kind", StringType(), True),
        StructField("etag", StringType(), True),
        StructField("id", StringType(), True),
        StructField("snippet", StructType([
            StructField("publishedAt", StringType(), True),
            StructField("channelId", StringType(), True),
            StructField("title", StringType(), True),
            StructField("description", StringType(), True),
            StructField("thumbnails", StructType([
                StructField("default", StructType([
                    StructField("url", StringType(), True),
                    StructField("width", IntegerType(), True),
                    StructField("height", IntegerType(), True),
                ]), True),
                # You can add other thumbnail types as needed
            ]), True),
            StructField("channelTitle", StringType(), True),
            StructField("tags", ArrayType(StringType()), True),
            StructField("categoryId", StringType(), True),
            StructField("liveBroadcastContent", StringType(), True),
            StructField("localized", StructType([
                StructField("title", StringType(), True),
                StructField("description", StringType(), True),
            ]), True),
            StructField("defaultAudioLanguage", StringType(), True),
        ]), True),
        StructField("contentDetails", StructType([
            StructField("duration", StringType(), True),
            StructField("dimension", StringType(), True),
            StructField("definition", StringType(), True),
            StructField("caption", StringType(), True),
            StructField("licensedContent", BooleanType(), True),
            StructField("contentRating", StringType(), True),
            StructField("projection", StringType(), True),
        ]), True),
        StructField("statistics", StructType([
            StructField("viewCount", StringType(), True),
            StructField("likeCount", StringType(), True),
            StructField("favoriteCount", StringType(), True),
            StructField("commentCount", StringType(), True),
        ]), True),
    ])
    return schema


def create_stream(spark, source_format, bootstrap_servers, topic, starting_offsets):
    return spark \
        .readStream \
        .format(source_format) \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .option("startingOffsets", starting_offsets) \
        .load()


def apply_schema(df, schema):
    return df.select(from_json(df.value.cast("string"), schema).alias("data"))


def process_df_and_group_by_category(df):
    return df.select("data.etag", "data.id", "data.snippet.*", "data.contentDetails.*", "data.statistics.*")


def start_kafka_stream():
    source_format = "kafka"
    bootstrap_servers = "kafka:9092"
    topic = "trending_videos"
    starting_offsets = "earliest"

    spark = init_spark()
    kafka_source_df = create_stream(spark, source_format, bootstrap_servers, topic, starting_offsets)

    schema = get_schema()
    processed_df = apply_schema(kafka_source_df, schema)

    grouped_df = process_df_and_group_by_category(processed_df)

    try:
        query = grouped_df \
            .writeStream \
            .outputMode("update") \
            .format("console") \
            .start()

        query.awaitTermination()
    except Exception as e:
        logger.error(f"An error occurred while starting the Kafka stream: {str(e)}", exc_info=True)


start_kafka_stream()
