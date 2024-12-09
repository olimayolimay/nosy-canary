import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Define intents
intents = discord.Intents.default()
intents.typing = False  # Optional: Disable typing events
intents.presences = False  # Optional: Disable presence updates
intents.messages = True  # Enable receiving message events
intents.message_content = True # Enable message content

# Pass intents to the bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(TOKEN)
