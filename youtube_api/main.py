import json

from apscheduler.schedulers.blocking import BlockingScheduler
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import NoBrokersAvailable
from retry import retry

from kafka_handler import KafkaHandler, KafkaTopic
from youtube_api_handler import YoutubeAPIHandler, Country


def fetch_and_push_trending_videos(youtube_api: YoutubeAPIHandler, kafka_handler: KafkaHandler, country: Country):
    """
    Fetches trending videos from the YouTube API for a specific country and pushes them to a Kafka topic.

    Parameters
    ----------
    youtube_api : YoutubeAPIHandler
        An instance of the YoutubeAPIHandler class that provides access to the YouTube API.
    kafka_handler : KafkaHandler
        An instance of the KafkaHandler class that handles interactions with Kafka.
    country : Country
        The country for which to fetch trending videos.

    Examples
    --------
    >>> youtube_api_handler = YoutubeAPIHandler()
    >>> kafka_ = KafkaHandler()
    >>> fetch_and_push_trending_videos(youtube_api_handler, kafka_, Country.UnitedStates)
    """
    next_token = None
    can_try = True

    while next_token or can_try:
        trending_videos, next_token = youtube_api.get_one_page_trending_video(country, next_token)
        trending_videos = [json.dumps(trending, indent=4) for trending in trending_videos]
        kafka_handler.send_json_array_to_kafka(trending_videos, KafkaTopic.trending_videos.value)
        can_try = False


NUM_PARTITIONS = 1
REPLICATION_FACTOR = 1


def main():
    """
    Initializes the scheduler, YouTube API, and Kafka handler.
    Then it schedules a job to fetch and push trending videos every 3 minutes.
    """
    try:
        scheduler = BlockingScheduler()

        youtube_api = YoutubeAPIHandler(api_service_name="youtube", api_version="v3", filename='secret.txt')
        kafka_handler = KafkaHandler("kafka", 9092)

        create_kafka_topics(kafka_handler.addr, kafka_handler.port)

        # Schedule the job to be called every 3 minutes
        scheduler.add_job(fetch_and_push_trending_videos,
                          'interval',
                          minutes=2,
                          args=[youtube_api, kafka_handler, Country.France])

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
    except FileNotFoundError:
        print("The 'secret.txt' file does not exist.")
    except PermissionError:
        print("Permission to 'secret.txt' denied.")


# retry on NoBrokersAvailable exception, total 20 tries with delay of 5 secs each
@retry(NoBrokersAvailable, tries=20, delay=5)
def create_kafka_topics(addr, port):
    print("Try to find brokers Available...")
    kafka_admin_client = KafkaAdminClient(bootstrap_servers=f'{addr}:{port}')
    new_topics = [NewTopic(name=topic.value, num_partitions=NUM_PARTITIONS, replication_factor=REPLICATION_FACTOR) for
                  topic in KafkaTopic if topic.value not in kafka_admin_client.list_topics()]
    kafka_admin_client.create_topics(new_topics=new_topics, validate_only=False)


if __name__ == "__main__":
    main()
