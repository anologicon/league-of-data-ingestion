import os
from typing import List
import datetime
import json

class LocalWriter:
    
    def write(self, summoners_data_list: List):
        for summoner_data in summoners_data_list:
            file_name = f'data/{summoner_data["summoner_data"]["summonerId"]}/{datetime.datetime.now().strftime("%Y-%m-%d")}.json'
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, "a") as f:
                f.write(json.dumps(summoner_data))
    