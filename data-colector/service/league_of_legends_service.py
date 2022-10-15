from requests import get, Response
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

class LeagueOfLegendsService:
    
    RANKED_SOLO_5x5_BASE_ENDPOINT = "league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    
    def __init__(self):
        self.default_header = {
            "content-type": "json",
            "X-Riot-Token": os.environ["LOL_API_KEY"],
        }
        self.base_url = "https://br1.api.riotgames.com/lol/"

    def fetch_challengers_summoners(self) -> List:
        return self.__base_request(
            self.__mount_url(self.RANKED_SOLO_5x5_BASE_ENDPOINT)
        )["entries"]

    def __mount_url(self, end_point: str) -> str:
        return self.base_url + end_point

    def __base_request(self, url: str):
        response = get(url, headers=self.default_header)
        response.raise_for_status()
        return response.json()
