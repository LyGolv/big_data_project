import csv
from typing import List, Dict
from kafka import KafkaProducer
from youtube_api_handler import YoutubeAPIHandler, Country


def convert_trending_videos_to_csv(trending_videos: List[Dict], categories: List[str], filename: str) -> None:
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['date', 'title', 'category', 'duration', 'viewCount', 'likeCount',
                         'dislikeCount', 'commentCount'])
        for video in trending_videos:
            writer.writerow([
                video['snippet']['publishedAt'],
                video['snippet']['title'],
                categories[video['snippet']['categoryId']],
                video['contentDetails']['duration'],
                video['statistics'].get('viewCount', 0),
                video['statistics'].get('likeCount', 0),
                video['statistics'].get('dislikeCount', 0),
                video['statistics'].get('commentCount', 0)
            ])


def send_file_to_kafka(filename: str) -> None:
    """
    This function sends the contents of a csv file to a kafka cluster running in a container.
    :param filename: The name of the file to send.
    :return: None
    """
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092')  # 'localhost:9092'
    with open(filename, 'r', encoding='utf-8') as file:
        while line := file.readline():
            print(line)
            producer.send('csv-trending-videos', value=line.encode('utf-8'))
    producer.flush()


def main():
    youtube_api = YoutubeAPIHandler(
        api_service_name="youtube",
        api_version="v3",
        api_key="AIzaSyBRmRt9euHeEOVtkrDVhif7wp51PIu3K3k"
    )
    categories = youtube_api.get_all_categories(Country.France)
    trending_videos = youtube_api.get_trending_videos(Country.France)
    filename = 'trending_videos.csv'
    convert_trending_videos_to_csv(trending_videos, categories, filename)
    send_file_to_kafka(filename)


if __name__ == "__main__":
    main()
