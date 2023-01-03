import logging
from repository.league_of_legends_repository import LeagueOfLegendsRepository
from service.base_request_service import BaseRequestService
from service.api.api_service import APIService
import pandas as pd
import json
from repository.data_writer.local_writer import LocalWriter
from repository.data_writer.minio_writer import MinioWriter
from concurrent import futures

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_MATCHES = 10
CHUNK_SIZE = 5


def main():
    print("Collecting challengers BR data - Max 200")
    api_service = APIService(
        LeagueOfLegendsRepository(BaseRequestService()), MAX_MATCHES, CHUNK_SIZE
    )
    writer = MinioWriter("league-of-data-raw")
    summoners_data_list = api_service.fetch_summoner_data(limit=200)
    with futures.ThreadPoolExecutor() as executor:
        executor.submit(api_service.fetch_summoner_mastery, summoners_data_list, writer)
        future_summoners_data_list = executor.submit(
            api_service.fetch_summoner_match, summoners_data_list, writer, 10
        )
        summoners_data_list = future_summoners_data_list.result()
        executor.submit(
            api_service.fetch_match_detail,
            summoners_data_list,
            writer,
        )
        executor.submit(
            api_service.fetch_match_timeline,
            summoners_data_list,
            writer,
        )


if __name__ == "__main__":
    main()
