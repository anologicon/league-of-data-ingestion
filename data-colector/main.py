from service.league_of_legends_service import LeagueOfLegendsService

def main():
    league_of_legends_service = LeagueOfLegendsService()
    print(league_of_legends_service.fetch_challengers_summoners())
    

if __name__ == "__main__":
    main()