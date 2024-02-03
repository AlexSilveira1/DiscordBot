#File        : proccess_league_data.py
#Description : This file handles all of the data processing for the league data. This includes getting the champion name, map name, and game mode.  
import json
import json

"""
Function    : convert_id_to_name
Description : This function takes in the id of a champion and returns the name to the caller. This is done by reading the json file of champions and finding an id match, then returning the name. 
Parameter   : id -> int of the champion id
Return      : str -> the champion name 
           : none if the champion is not found
"""
def convert_id_to_name(id):
    #open the json file containing all the champions data, using encoding utf8 as f 
    with open('riot\json\champions.json', encoding="utf8") as f:

        #using json, load the file contents making it a dictionary data type 
        content = json.load(f)

        #iterate over the contents of the file, and find the champion that has the matching id
        for i in range(len(content)): 

            #once the id and the champion id match 
            if str(id) == content[i]["key"]:
                #return the name of the champion 
                return content[i]["name"]
            
    #If champion was not found, we can return none 
    return None


"""
# Function      : get_map
# Description   : This function gets the name of the map 
# Parameters    : the queueId ->
# Return        : the name of the map or null 
"""
def get_map(queueId) -> str: 
    with open('riot\json\queueTypes.json', encoding="utf8") as f:
        content = json.load(f)
        for i in range(len(content)): 
            if int(queueId) == content[i]["queueId"]:
                 return content[i]["map"]
    return None 


"""
# Function      : get_mode
# Description   : Function gets the name of the game mode 
# Parameters    : queueId - > id of the queue 
# Return        : returns the game name or null 
"""
def get_mode(queueId) -> str: 
    with open('riot\json\queueTypes.json', encoding="utf8") as f:
        content = json.load(f)
        for i in range(len(content)): 
            if int(queueId) == content[i]["queueId"]:
                 return content[i]["description"]
    return None 

def process_ranked_data(data):
    
    if len(data) == 0:
        return "Unranked"

    # Process each league entry
    for entry in data:
        league_id = entry["leagueId"]
        queue_type = entry["queueType"]
        tier = entry["tier"]
        rank = entry["rank"]
        summoner_id = entry["summonerId"]
        summoner_name = entry["summonerName"]
        league_points = entry["leaguePoints"]
        wins = entry["wins"]
        losses = entry["losses"]
        veteran = entry["veteran"]
        inactive = entry["inactive"]
        fresh_blood = entry["freshBlood"]
        hot_streak = entry["hotStreak"]

        # Build the string with the extracted data
        result = f"League ID: {league_id}\n" \
                 f"Queue Type: {queue_type}\n" \
                 f"Tier: {tier}\n" \
                 f"Rank: {rank}\n" \
                 f"Summoner ID: {summoner_id}\n" \
                 f"Summoner Name: {summoner_name}\n" \
                 f"League Points: {league_points}\n" \
                 f"Wins: {wins}\n" \
                 f"Losses: {losses}\n" \
                 f"Veteran: {veteran}\n" \
                 f"Inactive: {inactive}\n" \
                 f"Fresh Blood: {fresh_blood}\n" \
                 f"Hot Streak: {hot_streak}\n\n"    
        return result