<<<<<<< HEAD
from click import command
import discord 
=======
import discord 
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix = "~", intents = intents )

async def command(ctx):
    await ctx.send()
    
>>>>>>> 2d2343c13cf35f27bb0d16785a931f2a04f75c62
