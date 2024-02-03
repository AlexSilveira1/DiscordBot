import requests
from riot import process_league_data as pld   # Import process_league_data.py from riot/process_riot_data

class RiotAPICaller:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_account_data(self, region, summoner_name):
        url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        data = self.make_api_call(url)
        return data

    def get_match_history_codes(self, region, summoner_name):
        """
        Gets match history for a given summoner name and region.

        Args:
        region (str): The region to search in.
        summoner_name (str): The summoner name to search for.

        Returns:
        list: A list of match IDs for the given summoner name and region.
        int: The HTTP status code if the request was unsuccessful.
        """
        account_data = self.get_account_data(summoner_name, region = None)
        if account_data is None:
            return None
        puuid = account_data.get("puuid")
        region_mapping = {
            "na1": "americas",
            "lan": "americas",
            "las": "americas",
            "kr": "asia",
            "pr": "asia",
            "eune": "europe",
            "euw": "europe",
            "tr": "europe",
            "ru": "europe",
            "oce": "sea",
            "ph2": "sea",
            "sg2": "sea",
            "th2": "sea",
            "tw2": "sea",
            "vn2": "sea"
        }
        region = region_mapping.get(region, region)
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{account_data['puuid']}/ids?start=0&count=5&api_key={self.api_key}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            match_history = response.json()
            return match_history
        else:
            return response.status_code

    def get_top_3_champions(self, region, summoner_name):
        """
        Gets the top 3 champions for a given summoner name and region.

        Args:
        region (str): The region to search in.
        summoner_name (str): The summoner name to search for.

        Returns:
        list: A list of the top 3 champions for the given summoner name and region.
        None: If the account data could not be retrieved.
        """
        account_data = self.get_account_data(region, summoner_name)
        if account_data is None:
            print("account data is none")
            return None
        puuid = account_data.get("puuid")
        api_call = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"
        
        data = self.make_api_call(api_call)
        
        top_3_champions = []
        for i in range(3):
            top_3_champions.append(pld.convert_id_to_name(data[i]["championId"]))
         
        return top_3_champions   


    def get_rank(self, region, summoner_name):
        """
        Gets the rank of a given summoner name and region.

        Args:
        api_key (str): The API key to use for making requests.
        region (str): The region to search in.
        summoner_name (str): The summoner name to search for.

        Returns:
        str: The rank of the given summoner name and region.
        None: If the rank could not be retrieved.
        """
        account_data = self.get_account_data(region, summoner_name)
        if account_data is None:
            return None
        id = account_data.get("id")
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"
        data = self.make_api_call(url)    
                
        return pld.proccess_ranked_data(data)   

    def get_match_history_data_from_code(self, code):
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{code}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        
        #use the json() function to get the data into variable 
        info = response.json()
        return info
    
    def get_match_history(self, region, summoner_name): 
        #get the account data for the summoner name
        summoner_data = self.get_account_data(region, summoner_name)
        #get the match history codes for the summoner name
        codes = self.get_match_history_codes(region, summoner_name)
        #get the match history data for the summoner name
        if codes is None:
            return None 
        all_match_history_info = []
        for code in codes:
            all_match_history_info.append(self.get_match_history_data_from_code(code))  

        return_info = []    
        game = []
        #find our player using their PUUID
        for x in range (len(all_match_history_info)):
            #find our player using their PUUID
            for i in range(len(all_match_history_info[x]["info"]["participants"])):
                if(all_match_history_info[x]["info"]["participants"][i]["puuid"] == summoner_data["puuid"]): 
                    #champion played
                    game.append(pld.convert_id_to_name(all_match_history_info[x]["info"]["participants"][i]["championId"]))
                    #game mode 
                    game.append(pld.get_mode(all_match_history_info[x]["info"]["queueId"]))
                    #win/loss
                    #CONVERT TRUE / FALSE TO VIC/DEF TEXT 
                    #game.append(all_match_history_info[x]["info"]["participants"][i]["win"])
                    if(all_match_history_info[x]["info"]["participants"][i]["win"] == True):
                        game.append("Victory")
                    else: 
                        game.append("Defeat")
                    #score
                    score = (f'{all_match_history_info[x]["info"]["participants"][i]["kills"]}/{all_match_history_info[x]["info"]["participants"][i]["deaths"]}/{all_match_history_info[x]["info"]["participants"][i]["assists"]}')
                    game.append(score)
                    #cs totalMinionsKilled	
                    cs = all_match_history_info[x]["info"]["participants"][i]["neutralMinionsKilled"] + all_match_history_info[x]["info"]["participants"][i]["totalMinionsKilled"]

                    game.append(cs)
                    #total gold
                    game.append(all_match_history_info[x]["info"]["participants"][i]["goldEarned"])
                    #map 
                    game.append(pld.get_map(all_match_history_info[x]["info"]["queueId"]))

                    return_info.append(game.copy())
                    game.clear()
        return return_info

    def get_league_stats(self, id):
        url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"
        data = self.make_api_call(url)
        return_data = pld.process_ranked_data(data) 
        return return_data  
    
    def make_api_call(self, url): 
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            account_data = response.json()
            return account_data
        else:
            return response.status_code  
        

# test code
# riot = RiotAPICaller("RGAPI-fbdc9af8-0c73-4063-bdb5-b9ee4034b5bd")
# data = riot.make_api_call("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/u5JmanR2jvcr_h-7jPC7PuKsJJvU6rnlTJvqZ1qtioXhwC4")
# print(data)
# print(riot.get_account_data("na1", "TSM Doublelift"))