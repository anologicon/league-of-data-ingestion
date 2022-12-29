from repository.league_of_legends_repository import LeagueOfLegendsRepository
from typing import List
from tqdm import tqdm
from repository.data_writer.writer_interface import WriterInterface
import re
import requests
import datetime
from concurrent import futures
import os
from random import randint
import time


class APIService:
    def __init__(
        self,
        league_of_legends_repository: LeagueOfLegendsRepository,
        max_matches=200,
        chunk_size=100,
    ) -> None:
        self.league_of_legends_repository = league_of_legends_repository
        self.max_matches = max_matches
        self.chunk_size = chunk_size

    def fetch_summoner_data(self, limit: int = None) -> List:
        summoners_list = self.league_of_legends_repository.fetch_challengers_summoners()

        if limit:
            summoners_list = summoners_list[:limit]

        summoner_with_details = []
        hash_table = {}
        with futures.ThreadPoolExecutor() as executor:
            to_do = []
            for summoner in summoners_list:
                hash_table[summoner["summonerName"]] = None
                if self.__summoner_has_special_characters(summoner["summonerName"]):
                    continue
                future = executor.submit(
                    self.league_of_legends_repository.fetch_summoner_details,
                    summoner,
                )
                to_do.append(future)
            results = []
            for future in tqdm(
                futures.as_completed(to_do),
                total=len(summoners_list),
                desc="Summoner details",
            ):
                res = future.result()
                results.append(res)

            for summoner_with_detail in results:
                if summoner_with_detail != None:
                    hash_table[summoner_with_detail["name"]] = summoner_with_detail

            executor.shutdown()

        for summoner in summoners_list:
            if hash_table[summoner["summonerName"]] != None:
                summoner_data = {
                    "summoner_detail": hash_table[summoner["summonerName"]],
                    "summoner_data": summoner,
                }
                summoner_with_details.append(summoner_data)

        return summoner_with_details

    def fetch_summoner_match(
        self, summoner_with_details: List, writer: WriterInterface, limit=None
    ):
        hash_table = {}
        with futures.ThreadPoolExecutor() as executor:
            to_do = []
            for summoner in summoner_with_details:
                future = executor.submit(
                    self.__search_summoner_match_ids, summoner, limit
                )
                to_do.append(future)
            results = []
            for future in tqdm(
                futures.as_completed(to_do),
                total=len(summoner_with_details),
                desc="Summoner matchs ids",
            ):
                res = future.result()
                results.append(res)

            for match in results:
                if match != None:
                    hash_table[match["summoner_id"]] = match["matches"]
            
            executor.shutdown()
            

        for summoner in summoner_with_details:
            if hash_table[summoner["summoner_detail"]["puuid"]] == None:
                continue

            summoner["matches"] = hash_table[summoner["summoner_detail"]["puuid"]]

            writer.write(
                f'summoners/summoner={summoner["summoner_data"]["summonerId"]}/extracted_at={datetime.datetime.now().strftime("%Y-%m-%d")}/{summoner["summoner_data"]["summonerId"]}_{datetime.datetime.now().strftime("%Y-%m-%d")}',
                summoner,
            )
        return summoner_with_details

    def __search_summoner_match_ids(self, summoner, limit=None):
        summoner_matches_id = []
        request_index = 0
        while request_index < self.max_matches:
            match_id_list = self.league_of_legends_repository.fetch_summoners_match_ids(
                summoner=summoner["summoner_detail"],
                request_index=request_index,
            )

            if limit:
                match_id_list = match_id_list[:limit]

            summoner_matches_id.extend(match_id_list)

            request_index += self.chunk_size
            if len(match_id_list) == 0:
                request_index = 400
        return {
            "summoner_id": summoner["summoner_detail"]["puuid"],
            "matches": summoner_matches_id,
        }

    def filter_unique_match_id(self, summoner_with_details_list: List) -> List:
        all_match_list = [
            match_id for x in summoner_with_details_list for match_id in x["matches"]
        ]
        return list(dict.fromkeys(all_match_list))

    def fetch_match_detail(self, match_ids, writer: WriterInterface) -> List:
        match_details = []
        for match_id in tqdm(match_ids, desc="Fetch Match Details"):
            match_details = self.league_of_legends_repository.fetch_match_data(
                match_id
            )
            writer.write(
                f'matchs/match={match_id}/extracted_at={datetime.datetime.now().strftime("%Y-%m-%d")}/{match_id}_{datetime.datetime.now().strftime("%Y-%m-%d")}',
                match_details)

    def __summoner_has_special_characters(self, summoner_name: str):
        regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
        if regex.search(summoner_name) != None:
            return True
        return False

    def __new_or_add_matches_from_summoner(
        self, summonerId, summoner_matches, match_id_list
    ):
        if summonerId not in summoner_matches:
            summoner_matches[summonerId] = match_id_list
            return summoner_matches
        summoner_matches[summonerId].extend(match_id_list)
        return summoner_matches
