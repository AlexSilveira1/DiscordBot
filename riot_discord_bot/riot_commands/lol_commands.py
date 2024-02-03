#import riot api caller
from riot.riot_api_caller import RiotAPICaller 


def league_handler (riot_api_caller, command, name, region=None):
    print(f'league_handler called with command {command} and name {name}, region {region}')
    if command == "lookup":
        valid_regions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
        return lookup_summoner(riot_api_caller=riot_api_caller, summoner_name=name, region=region)
        
            
         
def lookup_summoner(riot_api_caller, summoner_name, region=None):    
    if region is None:
        region = "na1"
        
    account_data = riot_api_caller.get_account_data(region=region, summoner_name=summoner_name)              
    #print(account_data)
    summoner_name = account_data.get("name")
    summoner_level = account_data.get("summonerLevel")
    
    league_stats = riot_api_caller.get_league_stats(id=account_data.get("id"))
    #print(league_stats)
    flex_winrate = (league_stats[0].get("wins")) / (league_stats[0].get("wins") + league_stats[0].get("losses"))
    soloq_winrate = (league_stats[1].get("wins")) / (league_stats[1].get("wins") + league_stats[1].get("losses"))
    
    top_champs = riot_api_caller.get_top_3_champions(region=region, summoner_name=summoner_name)
    
    my_string = f"""{summoner_name}: Level {summoner_level}
SOLO: {league_stats[1].get("tier")} {league_stats[1].get("rank")}: {league_stats[1].get("leaguePoints")} LP,\tWR: {soloq_winrate:.2%}
FLEX: {league_stats[0].get("tier")} {league_stats[0].get("rank")}: {league_stats[0].get("leaguePoints")} LP,\tWR: {flex_winrate:.2%}
TOP CHAMPIONS: {top_champs[0]}, {top_champs[1]}, {top_champs[2]}
"""
    return my_string
    
