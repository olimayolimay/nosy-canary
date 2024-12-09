import requests
import os
from dotenv import load_dotenv

load_dotenv()
YOUR_DISCORD_ID = os.getenv("YOUR_DISCORD_ID")
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

def create_task(discord_id, description, status='pending', notes=''):
    data = {
        "discord_id": discord_id,
        "description": description,
        "status": status,
        "notes": notes
    }
    r = requests.post(f"{API_BASE_URL}/api/tasks", json=data)
    if r.status_code == 201:
        print(f"Task created successfully! Task ID: {r.json()['task_id']}")
    else:
        print("Failed to create task. Response:", r.json())

def test_timer(discord_id):
    r = requests.get(f"{API_BASE_URL}/api/timer/{discord_id}")
    print("Timer response:", r.json())

if __name__ == "__main__":
    # Example usage: If not loading from .env file,
    # Replace 'YOUR_DISCORD_ID' with the actual Discord user ID you want to test with.
    my_discord_id = YOUR_DISCORD_ID

    # Create a new task for your user
    create_task(my_discord_id, "Write integration test instructions", status="pending", notes="No notes yet")

    # Optionally, test the timer endpoint
    test_timer(my_discord_id)

