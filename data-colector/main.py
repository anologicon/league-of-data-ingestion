import logging
from repository.league_of_legends_repository import LeagueOfLegendsRepository
from service.base_request_service import BaseRequestService
from service.api.api_service import APIService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    print("Collecting challengers BR data - Max 200")
    api_service = APIService(LeagueOfLegendsRepository(BaseRequestService()))
    summoners_data_list = api_service.fetch_summoner_data()
    summoner_matchs = api_service.fetch_summoner_match(summoners_data_list)
    summoner_matchs

    print("----- Match List ----")


if __name__ == "__main__":
    main()
