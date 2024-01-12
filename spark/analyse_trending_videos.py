import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, ArrayType, TimestampType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_spark():
    return (SparkSession.builder
            .master("spark://spark:7077")
            .appName("Analyze_trending_videos")
            .getOrCreate())


def get_schema():
    schema = StructType([
        StructField("kind", StringType(), True),
        StructField("etag", StringType(), True),
        StructField("id", StringType(), True),
        StructField("snippet", StructType([
            StructField("publishedAt", TimestampType(), True),
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
        .read \
        .format(source_format) \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .option("startingOffsets", starting_offsets) \
        .load()


def apply_schema(df, schema):
    return df.select(from_json(df.value.cast("string"), schema).alias("data"))


def process_df_and_group_by_category(df):
    new_df = df.select("data.etag", "data.id", "data.snippet.*", "data.contentDetails.*", "data.statistics.*")
    return new_df.groupBy("categoryId").count()


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
        # Assuming you have a DataFrame named df that you want to write to PostgreSQL
        # Replace the connection properties with your PostgreSQL database information

        jdbc_url = "jdbc:postgresql://postgres:5432/youtube_video"
        properties = {
            "user": "user",
            "password": "user",
            "driver": "org.postgresql.Driver"
        }

        # Write DataFrame to PostgreSQL table
        grouped_df.write.jdbc(url=jdbc_url, table="youtube_analysis", mode="overwrite", properties=properties)

        spark.stop()
    except Exception as e:
        logger.error(f"An error occurred while starting the Kafka stream: {str(e)}", exc_info=True)


start_kafka_stream()
