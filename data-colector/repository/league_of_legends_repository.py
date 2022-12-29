from requests import get, Response
import requests
from dotenv import load_dotenv
import os
from typing import List
from backoff import on_exception, expo
import ratelimit
import logging

load_dotenv()
from service.base_request_service import BaseRequestService


class LeagueOfLegendsRepository:
    def __init__(self, request_service: BaseRequestService):
        self.request_service = request_service

    RANKED_SOLO_5x5_BASE_ENDPOINT = (
        "league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    )
    MATCH_DATA = "match/v5/matches/{}"
    MATCH_TIME_LINE = "match/v5/matches/{}/timeline"
    SUMMONER_DATA = "summoner/v4/summoners/by-name/{}"
    MATCHES_IDS = "match/v5/matches/by-puuid/{}/ids?type=ranked&start={}&count={}"

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=250, period=10)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def fetch_match_data(self, match_id: int) -> List:
        return self.request_service.americas_request(self.MATCH_DATA.format(match_id))

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=250, period=10)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def fetch_match_time_line(self, match_id: int) -> List:
        return self.request_service.americas_request(
            self.MATCH_TIME_LINE.format(match_id)
        )

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def fetch_challengers_summoners(self) -> List:
        return self.request_service.brazil_request(self.RANKED_SOLO_5x5_BASE_ENDPOINT)[
            "entries"
        ]

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=1600, period=1)
    def fetch_summoner_details(self, summoner):
        try:
            return self.request_service.brazil_request(
                self.SUMMONER_DATA.format(summoner["summonerName"])
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=250, period=10)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def fetch_summoners_match_ids(
        self, summoner, request_index=0, max_return=100
    ) -> List:
        return self.request_service.americas_request(
            self.MATCHES_IDS.format(summoner["puuid"], request_index, max_return)
        )
