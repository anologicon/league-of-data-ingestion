from repository.league_of_legends_repository import LeagueOfLegendsRepository
from typing import List
from tqdm import tqdm


class APIService:

    def __init__(self, league_of_legends_repository: LeagueOfLegendsRepository, max_matches = 200, chunk_size = 100) -> None:
        self.league_of_legends_repository = league_of_legends_repository
        self.max_matches = max_matches
        self.chunk_size = chunk_size

    def fetch_summoner_data(self, limit: int = None) -> List:
        summoners_list = self.league_of_legends_repository.fetch_challengers_summoners()

        if limit:
            summoners_list = summoners_list[:limit]

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

    def fetch_summoner_match(self, summoner_with_details: List, limit=None):
        summoner_matches = {}
        for summoner in tqdm(summoner_with_details, desc="Summoner Matchs"):
            summoner_matches = self.__search_summoner_match_ids(
                summoner_matches, summoner, limit
            )
        for summoner_data in summoner_with_details:
            summoner_data["matches"] = summoner_matches[summoner_data["summoner_data"]["summonerId"]]
        return summoner_with_details

    def __search_summoner_match_ids(self, summoner_matches, summoner, limit=None):
        print(f"From summoner {summoner['summoner_data']['summonerName']}")
        request_index = 0
        while request_index < self.max_matches:
            print(f"Range {request_index} to {request_index + self.chunk_size}")
            match_id_list = self.league_of_legends_repository.fetch_summoners_match_ids(
                summoner=summoner["summoner_detail"],
                request_index=request_index,
            )

            if limit:
                match_id_list = match_id_list[:limit]

            summoner_matches = self.__new_or_add_matches_from_summoner(
                summoner["summoner_data"]["summonerId"],
                summoner_matches,
                self.__fetch_match_detail(match_id_list),
            )
            request_index += self.chunk_size
            if len(match_id_list) == 0:
                request_index = 400
        return summoner_matches

    def __fetch_match_detail(self, match_ids) -> List:
        match_details = []
        for match_id in match_ids:
            match_details.append(
                {
                    "match_data": self.league_of_legends_repository.fetch_match_data(match_id),
                    "match_time_line": self.league_of_legends_repository.fetch_match_time_line(match_id),
                    
                }
            )
        return match_details

    def __new_or_add_matches_from_summoner(
        self, summonerId, summoner_matches, match_id_list
    ):
        if summonerId not in summoner_matches:
            summoner_matches[summonerId] = match_id_list
            return summoner_matches
        summoner_matches[summonerId].extend(match_id_list)
        return summoner_matches
