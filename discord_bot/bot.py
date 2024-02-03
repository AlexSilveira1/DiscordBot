import discord 
from discord.ext import commands

"""
This file contains the logic to run a discord bot that will respond to user messages.
Any logic that is related to discord should be in this file.
Any logic that is related to the replies should be in responses.py
responses.py should not have any discord related logic and should only return message strings.
"""

class Bot:
    def __init__(self, discord_key):
        self.discord_key = discord_key
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)
        self.bot = commands.Bot(command_prefix='!', intents=self.intents)

    def run(self):
        @self.client.event
        async def on_ready(): 
            print(f'{self.client.user} is now running!')
        
        @self.bot.command
        async def ping(ctx):
            await ctx.send('pong!')

        self.bot.run(self.discord_key)