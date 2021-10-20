import discord
from discord.ext import commands
from src import GuildQueue


description = '''A bot used for coordinating pick up games with a variety of team sizes'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='~', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.command()
async def join(ctx):
    """Join the queue for a server"""

    output = GuildQueue.join(ctx)

    await ctx.send(output)


@bot.command()
async def queue(ctx):
    """Checks the queue"""

    output = GuildQueue.queue(ctx)

    await ctx.send(output)


@bot.command()
async def clear(ctx):
    """Clears the queue"""

    output = GuildQueue.clear(ctx)

    await ctx.send(output)


@bot.command()
async def finish(ctx):

    output = GuildQueue.finish(ctx)

    await ctx.send(output)



