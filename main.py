# File:          main.py
# Programmer:    Alex Silveira 
# First Version: 1.0 
# Date:          July 17th
# Description:   This is the main file of the program and simply runs the discord bot.
import configparser
from riot_discord_bot.riot_discord_bot import *   
# from discord_bot.bot import *  


def main():   
    config = configparser.ConfigParser()
    config.read('config.ini')

    discord_token = config['API_KEYS']['DISCORD_KEY']
    riot_api_key = config['API_KEYS']['RIOT_KEY']

    # bot = Bot(discord_token)
    # bot.run()

    rb = RiotDiscordBot(discord_token, riot_api_key)  
    rb.run()


if __name__ == '__main__':
    main() 
