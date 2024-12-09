import discord
from discord.ext import commands
from discord import app_commands, Embed
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set. Check your .env file or environment variables.")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="start", description="Initialize your user session or check user status")
async def start(interaction: discord.Interaction):
    # Placeholder response, could be improved to fetch user data from the backend.
    await interaction.response.send_message("Your session is ready!", ephemeral=True)

@bot.tree.command(name="setup", description="Set your canary bedtime or preferences")
async def setup_command(interaction: discord.Interaction):
    # Placeholder response, later can be replaced with user configuration logic.
    await interaction.response.send_message("Setup command received. You can configure your bedtime here.", ephemeral=True)

@bot.tree.command(name="tasks", description="List your current tasks")
async def tasks(interaction: discord.Interaction):
    discord_id = str(interaction.user.id)
    r = requests.get(f"{API_BASE_URL}/api/tasks/{discord_id}")
    data = r.json()
    tasks_data = data.get('tasks', [])

    if tasks_data:
        # Create a green embed for tasks
        embed = Embed(
            title="Your Tasks",
            description="Here are your current tasks:",
            color=0x00ff00  # Green
        )
        # Add a field for each task
        for task in tasks_data:
            embed.add_field(
                name=f"Task ID: {task['id']}",
                value=task['description'],
                inline=False
            )
    else:
        # Create a red embed if no tasks are found
        embed = Embed(
            title="Your Tasks",
            description="No tasks found.",
            color=0xff0000  # Red
        )

    # Add a footer and timestamp for a more polished look
    embed.set_footer(text="Nosy Canary Bot")
    embed.timestamp = datetime.utcnow()

    # Optionally, add an author or thumbnail if desired:
    # embed.set_author(name="Nosy Canary")
    # embed.set_thumbnail(url="https://example.com/image.png")

    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)

