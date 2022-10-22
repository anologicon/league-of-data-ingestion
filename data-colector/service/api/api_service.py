from repository.league_of_legends_repository import LeagueOfLegendsRepository
from typing import List
from tqdm import tqdm


class APIService:

    MAX_MATCHS = 300
    CHUNK_SIZE = 100

    def __init__(self, league_of_legends_repository: LeagueOfLegendsRepository) -> None:
        self.league_of_legends_repository = league_of_legends_repository

    def fetch_summoner_data(self) -> List:
        summoners_list = self.league_of_legends_repository.fetch_challengers_summoners()
        summoner_with_details = []
        for summoner in tqdm(summoners_list, desc="Summoner details"):
            summoner_data = {
                "summoner_detail": self.league_of_legends_repository.fetch_summoner_details(
                    summoner
                ),
                "summoner_data": summoner,
            }
            summoner_with_details.append(summoner_data)
        return summoner_with_details

    def fetch_summoner_match(self, summoner_with_details: List):
        summoner_matchs = {}
        for summoner in tqdm(summoner_with_details, desc="Summoner Matchs"):
            summoner_matchs = self.__search_summoner_match_ids(summoner_matchs, summoner)
        return summoner_matchs

    def __search_summoner_match_ids(self, summoner_matchs, summoner):
        print(f"From summoner {summoner['summoner_data']['summonerName']}")
        request_index = 0
        while request_index < self.MAX_MATCHS:
            print(f"Range {request_index} to {request_index + self.CHUNK_SIZE}")
            match_id_list = self.league_of_legends_repository.fetch_summoners_match_ids(
                summoner=summoner["summoner_detail"],
                request_index=request_index,
            )
            summoner_matchs = self.__new_or_add_matchs_from_summoner(
                summoner["summoner_data"]["summonerId"],
                summoner_matchs,
                match_id_list,
            )
            request_index += self.CHUNK_SIZE
            if len(match_id_list) == 0:
                request_index = 400
        return summoner_matchs

    def __new_or_add_matchs_from_summoner(
        self, summonerId, summoner_matchs, match_id_list
    ):
        if summonerId not in summoner_matchs:
            summoner_matchs[summonerId] = match_id_list
            return summoner_matchs
        summoner_matchs[summonerId].extend(match_id_list)
        return summoner_matchs
