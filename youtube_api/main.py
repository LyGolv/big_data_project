import csv

from youtube_api_handler import YoutubeAPIHandler, Country


def main():
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube_api = YoutubeAPIHandler(
        api_service_name="youtube",
        api_version="v3",
        api_key="AIzaSyBRmRt9euHeEOVtkrDVhif7wp51PIu3K3k"
    )

    all_categories = youtube_api.get_all_categories(Country.France)
    print(all_categories)
    trending_videos = youtube_api.get_trending_videos(Country.France)

    with open('trending_videos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['date', 'title', 'category', 'duration', 'viewCount', 'likeCount',
                         'dislikeCount', 'commentCount'])
        for video in trending_videos:
            writer.writerow([
                video['snippet']['publishedAt'],
                video['snippet']['title'],
                all_categories[video['snippet']['categoryId']],
                video['contentDetails']['duration'],
                video['statistics'].get('viewCount', 0),
                video['statistics'].get('likeCount', 0),
                video['statistics'].get('dislikeCount', 0),
                video['statistics'].get('commentCount', 0)
            ])


if __name__ == "__main__":
    main()
