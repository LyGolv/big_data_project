from enum import Enum

import googleapiclient.discovery


class Country(Enum):
    """
    Enumeration of country names and their ISO 3166-1 codes.
    """
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
    """
    Class responsible for handling YouTube API requests.
    """

    def __init__(self, api_service_name, api_version, filename):
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.api_key = YoutubeAPIHandler._read_api_key_from_file(filename)
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.api_key)

    @staticmethod
    def _read_api_key_from_file(filename: str) -> str:
        """
        Reads an API key from a file.

        Parameters
        ----------
        filename : str
            The name of the file to read the API key from

        Returns
        -------
        str
            The API key read from the file.
        """
        with open(filename, 'r') as file:
            return file.read().strip()

    def get_video_details(self, video_id: str):
        """
        Get details of a specific video.

        Parameters
        ----------
        video_id : str
            The ID of the video.

        Returns
        -------
        dict
            The response containing the video's details.
        """
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return response

    def get_videos_by_category(self, video_category: str):
        """
        Retrieves video details based on a specific category ID.

        Parameters
        ----------
        video_category : str
            The category ID of the videos to retrieve.

        Returns
        ------
        list
            A list containing details of all videos within the specified category.
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

    def get_trending_videos(self, region_code: Country):
        """
        Retrieves the trending videos for a specific region.

        Parameters
        ----------
        region_code : Country
            Enum which represent ISO 3166-1 code for the region to retrieve trending videos from.

        Returns
        -------
        list
            A list containing details of trending videos in the specified region.
        """
        trending_videos = []
        response, next_token = self.get_one_page_trending_video(region_code)
        trending_videos.extend(response)
        while next_token:
            response, next_token = self.get_one_page_trending_video(region_code, next_token)
            trending_videos.extend(response)
        return trending_videos

    def get_one_page_trending_video(self, region_code: Country, page_token=None):
        """
        Retrieves the trending videos on YouTube for a specific region and page.

        Parameters
        ----------
        region_code : Country
            An Enum representing the region for which the trending videos are to be fetched.
        page_token : str, optional
            The page token for the next page of results. If not provided, the first page of results will be fetched.

        Returns
        -------
        tuple
            A tuple containing two elements:
            - items: The list of trending videos on YouTube for the specified region and page.
            - nextPageToken: The page token for the next page of results. If there are no more pages, this will be None.
        """
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code.value,
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()
        return response['items'], response.get('nextPageToken', None)

    def get_all_categories(self, region_code: Country):
        """
        Retrieves all the categories of videos for a specific region.

        Parameters
        ----------
        region_code : Country
            An Enum which represents the region for which video categories are to be retrieved.

        Returns
        -------
        dict
            A dictionary where the keys are category IDs and the values are category titles.
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
