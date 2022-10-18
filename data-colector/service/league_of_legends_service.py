from requests import get, Response
import requests
from dotenv import load_dotenv
import os
from typing import List
from backoff import on_exception, expo
import ratelimit
import logging
load_dotenv()

class LeagueOfLegendsService:
    
    BASE_BR_URL = "https://br1.api.riotgames.com/lol/"
    BASE_AMERICA_URL = "https://americas.api.riotgames.com/lol/"
    RANKED_SOLO_5x5_BASE_ENDPOINT = "league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    SUMMONER_DATA = "summoner/v4/summoners/by-name/{}"
    MATCHS_IDS = "match/v5/matches/by-puuid/{}/ids?type=ranked&start={}&count={}"
    
    def __init__(self):
        self.default_header = {
            "content-type": "json",
            "X-Riot-Token": os.environ["LOL_API_KEY"],
        }

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def fetch_challengers_summoners(self) -> List:
        return self.__base_request(
            self.__mount_br_url(self.RANKED_SOLO_5x5_BASE_ENDPOINT)
        )["entries"]
    
    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=1600, period=60)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def fetch_summoner_details(self, summoner):
        return self.__base_request(
            self.__mount_br_url(self.SUMMONER_DATA.format(
                summoner["summonerName"]))
        )
    
    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=250, period=10)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def fetch_summoners_match_ids(self, summoner, request_index = 0, max_return = 100) -> List:
        return self.__base_request(
            self.__mount_americas_url(self.MATCHS_IDS.format(
                summoner["puuid"], request_index, max_return))
        )

    def __mount_americas_url(self, end_point: str) -> str:
        return self.BASE_AMERICA_URL + end_point

    def __mount_br_url(self, end_point: str) -> str:
        return self.BASE_BR_URL + end_point

    def __base_request(self, url: str):
        response = get(url, headers=self.default_header)
        response.raise_for_status()
        return response.json()
