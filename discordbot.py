import discord 
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix = "~", intents = intents )

async def command(ctx):
    await ctx.send()
    