import googleapiclient.discovery
from enum import Enum


class Country(Enum):
    """Enumeration of country names and their ISO 3166-1 codes."""
    UnitedStates = 'US'
    UnitedKingdom = 'GB'
    India = 'IN'
    France = 'FR'
    Canada = 'CA'
    Germany = 'DE'
    Australia = 'AU'
    Brazil = 'BR'
    Japan = 'JP'
    SouthKorea = 'KR'
    Belgium = 'BE'


class YoutubeAPIHandler:
    """Class responsible for handling YouTube API requests."""

    def __init__(self, api_service_name, api_version, filename):
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.api_key = self._read_api_key_from_file(filename)
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.api_key)

    @staticmethod
    def _read_api_key_from_file(filename: str) -> str:
        """
        Reads an API key from a file.

        :param filename: The name of the file to read the API key from.
        :type filename: str
        :return: The API key read from the file.
        :rtype: str
        """
        with open(filename, 'r') as file:
            return file.read().strip()

    def get_video_details(self, video_id):
        """
        Get details of a specific video.

        :param video_id: The ID of the video.
        :return: The response containing the video's details.
        """
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return response

    def get_videos_by_category(self, video_category):
        """
        :param video_category: The category ID of the videos to retrieve. The category ID is a string that represents
        a specific category.
        :return: A list of video details. Each video detail is a dictionary containing
        information about a video.
        """
        request = self.youtube.search().list(
            part="snippet",
            type="video",
            videoCategoryId=video_category
        )
        response = request.execute()
        video_details = []
        for item in response['items']:
            video_details.append(self.get_video_details(item['id']['videoId']))
        return video_details

    def get_trending_videos(self, region_code):
        """
        Get the most trending videos in a specific region.

        :param region_code: The region code indicating the desired region.
        :return: A list of dictionaries representing the trending videos.
        """
        trending_videos = []
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code.value,
            maxResults=50
        )
        response = request.execute()
        next_token = response.get('nextPageToken', None)
        trending_videos.extend(response['items'])
        while next_token:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                chart="mostPopular",
                regionCode=region_code.value,
                maxResults=50,
                pageToken=next_token
            )
            response = request.execute()
            next_token = response.get('nextPageToken', None)
            trending_videos.extend(response['items'])
        return trending_videos

    def get_all_categories(self, region_code):
        """
        :param region_code: A region code that represents the desired region for retrieving video categories.
        :return: A dictionary where the keys are category IDs and the values are category titles.
        """
        categories = {}
        request = self.youtube.videoCategories().list(
            part="snippet",
            regionCode=region_code.value
        )
        response = request.execute()
        for item in response['items']:
            categories[item['id']] = item['snippet']['title']
        return categories
