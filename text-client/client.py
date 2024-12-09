import requests

BASE_URL = "http://localhost:5000"

def list_tasks(discord_id):
    r = requests.get(f"{BASE_URL}/api/tasks/{discord_id}")
    return r.json()

if __name__ == "__main__":
    # Simple CLI simulation:
    # E.g., "python client.py list_tasks 123456789"
    import sys
    command = sys.argv[1]
    if command == "list_tasks":
        discord_id = sys.argv[2]
        tasks = list_tasks(discord_id)
        print(tasks)

