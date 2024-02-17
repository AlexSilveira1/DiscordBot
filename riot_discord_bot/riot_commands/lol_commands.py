#import riot api caller
from riot.riot_api_caller import RiotAPICaller 


def league_handler (riot_api_caller, command, name, region=None):
    print(f'league_handler called with command {command} and name {name}, region {region}')
    if command == "lookup":
        valid_regions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
        return lookup_summoner(riot_api_caller=riot_api_caller, summoner_name=name, region=region)
    elif command == "match_history":
        return lookup_match_history(riot_api_caller=riot_api_caller, summoner_name=name, region=region)
        
            
         
def lookup_summoner(riot_api_caller, summoner_name, region=None):    
    print(f'lookup_summoner called with summoner_name {summoner_name} and region {region}')
    if region is None:
        region = "na1"
        
    account_data = riot_api_caller.get_account_data(region=region, summoner_name=summoner_name)    
    print(f"Account data: {account_data}")   
    summoner_name = account_data.get("name")
    summoner_level = account_data.get("summonerLevel")
    print(f"Summoner name: {summoner_name}, level: {summoner_level}")
    top_champs = riot_api_caller.get_top_3_champions(region=region, summoner_name=summoner_name)
    print(f"Top 3 champions: {top_champs}")
    #format the leaguye stats data, ensure that solo queue is first then flex queue
    solo_queue = ""
    flex_queue = ""
    win_rate = ""
    
    league_stats = riot_api_caller.get_rank(region=region, summoner_name=summoner_name)
    print(f"League stats data type: {type(league_stats)}")
    for entry in league_stats:
        if entry["queueType"] == "RANKED_SOLO_5x5":
            solo_queue = f"Solo/Duo: {entry['tier']} {entry['rank']} {entry['leaguePoints']} LP"
            solo_win_rate = f"Win Rate: {entry['wins'] / (entry['wins'] + entry['losses']) * 100:.2f}%"
            solo_wins = f"Wins: {entry['wins']}"
            solo_losses = f"Losses: {entry['losses']}"
        elif entry["queueType"] == "RANKED_FLEX_SR":
            flex_queue = f"Flex: {entry['tier']} {entry['rank']} {entry['leaguePoints']} LP"
            flex_win_rate = f"Win Rate: {entry['wins'] / (entry['wins'] + entry['losses']) * 100:.2f}%" 
            flex_wins = f"Wins: {entry['wins']}"
            flex_losses = f"Losses: {entry['losses']}"  
    
    my_string = f"""{summoner_name}: Level {summoner_level}
Top Champions: {top_champs[0]}, {top_champs[1]}, {top_champs[2]}
Ranked Stats:
\t{solo_queue} {solo_wins} {solo_losses} {solo_win_rate}
\t{flex_queue} {flex_wins} {flex_losses} {flex_win_rate}
"""    

    return my_string

def lookup_match_history(riot_api_caller, summoner_name, region=None):
    if region is None:
        region = "na1"
    match_history = riot_api_caller.get_match_history(region=region, summoner_name=summoner_name)
    return match_history
