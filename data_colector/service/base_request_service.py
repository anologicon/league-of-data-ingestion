from requests import get, Response
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class BaseRequestService:

    BASE_BR_URL = "https://br1.api.riotgames.com/lol/"
    BASE_AMERICA_URL = "https://americas.api.riotgames.com/lol/"

    def __init__(self) -> None:
        self.default_header = {
            "content-type": "json",
            "X-Riot-Token": os.environ["LOL_API_KEY"],
        }

    def americas_request(self, url: str):
        return self.__base_request(self.__mount_americas_url(url))

    def brazil_request(self, url: str):
        return self.__base_request(self.__mount_br_url(url))

    def __base_request(self, url: str):
        response = get(url, headers=self.default_header)
        response.raise_for_status()
        return response.json()

    def __mount_americas_url(self, end_point: str) -> str:
        return self.BASE_AMERICA_URL + end_point

    def __mount_br_url(self, end_point: str) -> str:
        return self.BASE_BR_URL + end_point
