import discord
from discord.ext import commands
from discord import app_commands, Embed
import os
from dotenv import load_dotenv
import aiohttp
import asyncio
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set. Check your .env file or environment variables.")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
GUILD_ID = os.getenv("GUILD_ID")

if GUILD_ID is None:
    raise ValueError("GUILD_ID is not set. Please add it to your .env file.")

try:
    GUILD_ID = int(GUILD_ID)
except ValueError:
    raise ValueError("GUILD_ID must be an integer.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild ID {GUILD_ID}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

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
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/api/tasks/{discord_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
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
                                value=f"**Description:** {task['description']}\n**Status:** {task['status']}\n**Notes:** {task['notes']}",
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

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        error_data = await resp.json()
                        error_message = error_data.get('error', 'Unknown error')
                    except Exception:
                        error_message = 'Unknown error'

                    await interaction.response.send_message(
                        f"Error fetching tasks: {error_message}",
                        ephemeral=True
                    )
        except aiohttp.ClientError as e:
            await interaction.response.send_message(
                f"Failed to connect to the backend API: {e}",
                ephemeral=True
            )

@bot.tree.command(name="addtask", description="Add a new task with a description")
@app_commands.describe(description="The description of the task to add")
async def addtask(interaction: discord.Interaction, description: str):
    discord_id = str(interaction.user.id)
    payload = {
        "discord_id": discord_id,
        "description": description
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/api/tasks", json=payload) as resp:
                if resp.status == 201:
                    data = await resp.json()
                    task_id = data.get('task_id', 'N/A')
                    
                    embed = Embed(
                        title="Task Added Successfully!",
                        color=0x00ff00  # Green
                    )
                    embed.add_field(name="Task ID", value=str(task_id), inline=True)
                    embed.add_field(name="Description", value=description, inline=False)
                    embed.set_footer(text="Nosy Canary Bot")
                    embed.timestamp = datetime.utcnow()
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        error_data = await resp.json()
                        error_message = error_data.get('error', 'Unknown error')
                    except Exception:
                        error_message = 'Unknown error'
                    
                    embed = Embed(
                        title="Failed to Add Task",
                        description=error_message,
                        color=0xff0000  # Red
                    )
                    embed.set_footer(text="Nosy Canary Bot")
                    embed.timestamp = datetime.utcnow()
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        except aiohttp.ClientError as e:
            embed = Embed(
                title="Connection Error",
                description=f"❌ Failed to connect to the backend API: {e}",
                color=0xff0000  # Red
            )
            embed.set_footer(text="Nosy Canary Bot")
            embed.timestamp = datetime.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="edittask", description="Edit the description of an existing task")
@app_commands.describe(
    task_id="The ID of the task to edit",
    new_description="The new description for the task"
)
async def edittask(interaction: discord.Interaction, task_id: int, new_description: str):
    payload = {
        "description": new_description
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(f"{API_BASE_URL}/api/tasks/{task_id}", json=payload) as resp:
                if resp.status == 200:
                    embed = Embed(
                        title="Task Updated Successfully!",
                        color=0x00ff00  # Green
                    )
                    embed.add_field(name="Task ID", value=str(task_id), inline=True)
                    embed.add_field(name="New Description", value=new_description, inline=False)
                    embed.set_footer(text="Nosy Canary Bot")
                    embed.timestamp = datetime.utcnow()
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        error_data = await resp.json()
                        error_message = error_data.get('error', 'Unknown error')
                    except Exception:
                        error_message = 'Unknown error'
                    
                    embed = Embed(
                        title="Failed to Update Task",
                        description=error_message,
                        color=0xff0000  # Red
                    )
                    embed.set_footer(text="Nosy Canary Bot")
                    embed.timestamp = datetime.utcnow()
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        except aiohttp.ClientError as e:
            embed = Embed(
                title="Connection Error",
                description=f"❌ Failed to connect to the backend API: {e}",
                color=0xff0000  # Red
            )
            embed.set_footer(text="Nosy Canary Bot")
            embed.timestamp = datetime.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="deletetask", description="Delete a specified task by ID")
@app_commands.describe(task_id="The ID of the task to delete")
async def deletetask(interaction: discord.Interaction, task_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(f"{API_BASE_URL}/api/tasks/{task_id}") as resp:
                if resp.status == 200:
                    embed = Embed(
                        title="Task Deleted Successfully!",
                        color=0x00ff00  # Green
                    )
                    embed.add_field(name="Task ID", value=str(task_id), inline=True)
                    embed.set_footer(text="Nosy Canary Bot")
                    embed.timestamp = datetime.utcnow()
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        error_data = await resp.json()
                        error_message = error_data.get('error', 'Unknown error')
                    except Exception:
                        error_message = 'Unknown error'
                    
                    embed = Embed(
                        title="Failed to Delete Task",
                        description=error_message,
                        color=0xff0000  # Red
                    )
                    embed.set_footer(text="Nosy Canary Bot")
                    embed.timestamp = datetime.utcnow()
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        except aiohttp.ClientError as e:
            embed = Embed(
                title="Connection Error",
                description=f"❌ Failed to connect to the backend API: {e}",
                color=0xff0000  # Red
            )
            embed.set_footer(text="Nosy Canary Bot")
            embed.timestamp = datetime.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)

