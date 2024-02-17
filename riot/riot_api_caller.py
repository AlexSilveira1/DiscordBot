import requests
from riot import process_league_data as pld   # Import process_league_data.py from riot/process_riot_data
               
# Method to validate the region input   
def validate_region(region):
    valid_regions = ["americas", "asia", "europe"]
    if region not in valid_regions:
        raise False
    
def valid_regions_shorthand(region):
    valid_regions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "ph2", "ru", "sg2", "th2", "tr1", "tw2", "vn2","oc1", "tr1"]
    if region not in valid_regions:
        return False
    return True

def valid_queue_types(queue):
    valid_queues = ["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT", "RANKED_TFT"]
    if queue not in valid_queues:
        return False
    return True

def valid_ranks(rank):
    valid_ranks = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
    if rank not in valid_ranks:
        return False
    return True

def valid_divisions(division):
    valid_divisions = ["I", "II", "III", "IV"]
    if division not in valid_divisions:
        return False
    return True

# Riot API Caller class
class RiotAPICaller:
    def __init__(self, api_key):
        self.api_key = api_key
        
    #Methods to get the data from the Riot API
    def get_account_data_by_puuid(self, puuid, region="americas"): 
        if validate_region(region) == False:
            region = "americas"
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
        return make_api_call(url)
    
    def get_account_data_by_name_and_tagline(self, summoner_name, tagline, region="americas"):
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagline}"
        return self.make_api_call(url)
    
    def get_active_shards_by_game_and_puuid(self, game, puuid, region="americas"):
        url = f"https://{region}.api.riotgames.com/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}"
        return self.make_api_call(url)
    
    # Methods to get champion mastery data
    def get_champion_mastery_data_by_puuid(self, puuid, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"      
        url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
        return self.make_api_call(url)
    
    def get_champion_mastery_data_by_puuid_and_champion(self, puuid, champion_id, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}"
        return self.make_api_call(url)
    
    def get_top_champion_mastery_data_by_puuid(self, puuid, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"
        return self.make_api_call(url)
    
    def get_champion_mastery_score_by_puuid(self, puuid, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/scores/by-puuid/{puuid}"
        return self.make_api_call(url)
    
    #Method for getting free champion rotation
    def get_free_champion_rotation(self, region="americas"):
        if valid_regions_shorthand(region) == False:  
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/platform/v3/champion-rotations"
        return self.make_api_call(url)
    
    #Methods for clash
    def get_account_data_by_name_and_tagline(self, summoner_name, tagline, region="na1"):
        if validate_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagline}"
        return self.make_api_call(url)
    
    def get_clash_team_data(self, team_id, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/clash/v1/teams/{team_id}"
        return self.make_api_call(url)
    
    def get_clash_tournaments(self, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/clash/v1/tournaments"
        return self.make_api_call(url)
    
    def get_clash_tournaments_by_team(self, team_id, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/clash/v1/tournaments/by-team/{team_id}"
        return self.make_api_call(url)
    
    def get_clash_tournament_data(self, tournament_id, region="na1"):
        if valid_regions_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/clash/v1/tournaments/{tournament_id}"
        return self.make_api_call(url)
    
    def get_league_entries(self, queue, tier, division, region="na1"):
        if valid_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}"
        return self.make_api_call(url)
    
    def get_league_entries_by_page(self, queue, tier, division, page=1, region="na1"):
        if not valid_regions_shorthand(region) or not valid_queue_types(queue) or not valid_ranks(tier) or not valid_divisions(division):
            return "Invalid input parameters"
        
        url = f"https://{region}.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page={page}"
        return self.make_api_call(url)
    
    #League-v4
    def get_challenger_league_data(self, queue, region="na1"):
        if not valid_regions_shorthand(region) or not valid_queue_types(queue):
            return "Invalid input parameters"
        
        url = f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}"
        return self.make_api_call(url)
    
    def get_league_entries_by_summoner(self, summoner_id, region="na1"):
        if valid_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        return self.make_api_call(url)

    def get_league_entries(self, queue, tier, division, region="na1"):
        if validate_region(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}"
        return self.make_api_call(url)
    
    def get_grandmaster_league_data(self, queue, region="na1"):
        if not valid_regions_shorthand(region) or not valid_queue_types(queue):
            return "Invalid input parameters"
        
        url = f"https://{region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}"
        return self.make_api_call(url)

    def get_league_data(self, league_id, region="na1"):
        if valid_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/league/v4/leagues/{league_id}"
        return self.make_api_call(url)
    
    def get_master_league_data(self, queue, region="na1"):
        if not valid_regions_shorthand(region) or not valid_queue_types(queue):
            return "Invalid input parameters"
        
        url = f"https://{region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queue}"
        return self.make_api_call(url)
    
    #Lol-challenges-v1
    def get_challenges_config(self, region="na1"):
        if validate_region(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/challenges/v1/challenges/config"
        return self.make_api_call(url)
    
    def get_challenges_percentiles(self, region="na1"):
        if valid_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/challenges/v1/challenges/percentiles"
        return self.make_api_call(url)

    def get_challenge_config_by_challenge_id(self, challenge_id, region="na1"):
        if validate_region(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/challenges/v1/challenges/{challenge_id}/config"
        return self.make_api_call(url)
    
    def get_challenge_leaderboards_by_level(self, challenge_id, level, region="na1"):
        if valid_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/challenges/v1/challenges/{challenge_id}/leaderboards/by-level/{level}"
        return self.make_api_call(url)

    def get_challenge_percentiles(self, challenge_id, region="na1"):
        if validate_region(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/challenges/v1/challenges/{challenge_id}/percentiles"
        return self.make_api_call(url)

    def get_challenge_player_data(self, puuid, region="na1"):
        if valid_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/challenges/v1/player-data/{puuid}"
        return self.make_api_call(url)

    #Lol Status v4
    def get_platform_data(self, region="na1"):
        if valid_region_shorthand(region) == False:
            region = "na1"
        url = f"https://{region}.api.riotgames.com/lol/status/v4/platform-data"
        return self.make_api_call(url)
    
    #Match-v5 
    def get_match_ids_by_puuid(self, puuidregion="americas"):
        if validate_region(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
            
    def get_match_data_by_id(self, match_id, region="americas"):
        if validate_region(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
            return self.make_api_call(url)
        
    def get_match_timeline_by_id(self, match_id, region="americas"):
        if validate_region(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
            return self.make_api_call(url)
        
    #spectator-v4
    def get_active_games_by_summoner(self, summoner_id, region="na1"):
        if valid_regions_shorthand(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
            return self.make_api_call(url)
        
    def get_featured_games(self, region="na1"):
        if valid_regions_shorthand(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/spectator/v4/featured-games"
            return self.make_api_call(url)
    
    
    #summoner-v4  
    def get_summoner_data_by_account_id(self, account_id, region="na1"):
        if valid_regions_shorthand(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{account_id}"
            return self.make_api_call(url)
        
    def get_summoner_data_by_name(self, summoner_name, region="na1"):
        if valid_regions_shorthand(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
            return self.make_api_call(url)
        
        
    def get_summoner_data_by_puuid(self, puuid, region="na1"):
        if valid_regions_shorthand(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
            return self.make_api_call(url)
        
    def get_summoner_data_by_summoner_id(self, summoner_id, region="na1"):
        if valid_regions_shorthand(region) == False:
            url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
            return self.make_api_call(url) 
        
        
    #Old calls 
    def get_account_data(self, region, summoner_name):
        url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        data = self.make_api_call(url)
        return data

    def get_match_history_codes(self, region, summoner_name):
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
        account_data = self.get_account_data(region, summoner_name)
        if account_data is None:
            return None
        id = account_data.get("id")
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"
        return self.make_api_call(url)  

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