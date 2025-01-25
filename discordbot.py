import discord 

from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix = "~", intents = intents )

@bot.command()
async def command(ctx):
    await ctx.send("hello! you used '~command'!")
    print(yes)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run('..')
    
