from discord_bot.bot import *
from riot.riot_api_caller import RiotAPICaller
from riot_discord_bot.riot_commands.lol_commands import league_handler as league_handler
from riot_discord_bot.riot_commands import val_commands as val
from riot_discord_bot.riot_commands import tft_commands as tft
from riot_discord_bot.riot_commands import lor_commands as lor

#every command function will follow a simple format
#the command will be !riot <command> <args>


class RiotDiscordBot(Bot):
    def __init__(self, discord_key, riot_key):
        super().__init__(discord_key)
        print('RiotDiscordBot initialized')
        self.riot_key = riot_key
        self.RiotCaller = RiotAPICaller(self.riot_key)

    def run(self):
        @self.client.event
        async def on_ready():
            print(f'{self.client.user} is now running!')

        @self.bot.command()
        async def hello(ctx):
            print(f"Message received: {ctx.message.content}")
            await ctx.send('hi!')

        @self.bot.command()
        async def lol(ctx, *args):
            for i in range(len(args)):
                print(f'{i}: {args[i]}')
            if len(args) == 0:
                await ctx.send("No command given. Use lol help for a list of commands.")
                return
            
            command = args[0]
            region = args[1]
            name = ' '.join(args[2:])
            output = league_handler(riot_api_caller=self.RiotCaller, command=command, name=name, region=region)
            await ctx.send(output)
            
        @self.bot.command()
        async def val(ctx, *args):
            if len(args) == 0:
                await ctx.send("No command given. Use lol help for a list of commands.")
                return
            await ctx.send(' '.join(args))

        @self.bot.command()
        async def tft(ctx, *args):
            if len(args) == 0:
                await ctx.send("No command given. Use lol help for a list of commands.")
                return
            print(args)
            await ctx.send(' '.join(args))

        @self.bot.command()
        async def lor(ctx, *args):
            if len(args) == 0:
                await ctx.send("No command given. Use lol help for a list of commands.")
                return
            print(args)
            await ctx.send(' '.join(args))

        self.bot.run(self.discord_key)   