import logging
from service.league_of_legends_service import LeagueOfLegendsService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    print("Collecting challengers BR data - Max 200")
    league_of_legends_service = LeagueOfLegendsService()
    summoners_list = league_of_legends_service.fetch_challengers_summoners()
    summoner_with_details = []
    for summoner in summoners_list:
        print(f"Summoner details from {summoner['summonerName']}")
        summoner_data = {
            'summoner_detail': league_of_legends_service.fetch_summoner_details(summoner),
            'summoner_data': summoner
        }
        summoner_with_details.append(summoner_data)
    summoner_matchs = {}
    for summoner in summoner_with_details:
        keep_request = True
        request_index = 0
        while(keep_request):
            match_id_list = league_of_legends_service.fetch_summoners_match_ids(
                summoner=summoner['summoner_detail'],
                request_index=request_index
            )
            if summoner["summoner_data"]["summonerId"] not in summoner_matchs:
                summoner_matchs[summoner["summoner_data"]["summonerId"]] = match_id_list
            else:
                summoner_matchs[summoner["summoner_data"]["summonerId"]].extend(match_id_list)
            request_index += 100
            if len(match_id_list) == 0:
                keep_request = False
            
        
    



if __name__ == "__main__":
    main()