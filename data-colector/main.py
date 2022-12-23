import logging
from repository.league_of_legends_repository import LeagueOfLegendsRepository
from service.base_request_service import BaseRequestService
from service.api.api_service import APIService
import pandas as pd
import json
from repository.data_writer.local_writer import LocalWriter
from repository.data_writer.minio_writer import MinioWriter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_MATCHES = 100
CHUNK_SIZE = 50


def main():
    print("Collecting challengers BR data - Max 200")
    api_service = APIService(
        LeagueOfLegendsRepository(BaseRequestService()), MAX_MATCHES, CHUNK_SIZE
    )
    summoners_data_list = api_service.fetch_summoner_data(limit=200)
    print("----- Match List ----")
    summoners_data_list = api_service.fetch_summoner_match(
        summoners_data_list, MinioWriter("league-of-data-raw")
    )


if __name__ == "__main__":
    main()
