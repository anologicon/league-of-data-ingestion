import logging
from repository.league_of_legends_repository import LeagueOfLegendsRepository
from service.base_request_service import BaseRequestService
from service.api.api_service import APIService
import pandas as pd
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    print("Collecting challengers BR data - Max 200")
    api_service = APIService(LeagueOfLegendsRepository(BaseRequestService()))
    summoners_data_list = api_service.fetch_summoner_data(limit=10)
    print("----- Match List ----")
    summoner_matches = api_service.fetch_summoner_match(
        summoners_data_list, limit=10)
    for summoner_data in summoners_data_list:
        summoner_data["matches"] = summoner_matches[summoner_data["summoner_data"]["summonerId"]]
    json_data = []
    for summoner_data in summoners_data_list:
        json_data.append({
            "summonerId": summoner_data["summoner_data"]["summonerId"],
            "raw_data": json.dumps(summoner_data)
        })
    df = pd.DataFrame(json_data, columns=['summonerId', "raw_data"])
    df.to_csv('data.csv', index=False)

if __name__ == "__main__":
    main()
