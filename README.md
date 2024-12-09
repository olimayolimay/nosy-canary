# Nosy Canary

**Nosy Canary** is a productivity tool that helps users manage their habits, daily intentions, and tasks through scheduled prompts and interactive workflows. This repository contains a Flask-based backend, a Discord bot as the primary frontend, and a simple text-based client for testing.

## Project Structure

```
nosy-canary/
├─ backend/
│  ├─ venv/          # Python virtual environment for the backend
│  ├─ app.py          # Main Flask app
│  ├─ models.py       # SQLAlchemy models
│  ├─ routes/         # Blueprint routes for tasks, intentions, etc.
│  ├─ requirements.txt # Backend dependencies
│  └─ ...             
├─ frontend/
│  ├─ venv/           # Python virtual environment for the Discord bot
│  ├─ bot.py          # Discord bot main script
│  ├─ requirements.txt # Bot dependencies
│  └─ .env             # Environment variables (e.g., DISCORD_TOKEN)
└─ text-client/
   ├─ venv/            # Optional virtual environment for text client
   ├─ client.py        # CLI script to test backend endpoints
   ├─ requirements.txt # Text client dependencies
   └─ ...
```

## Prerequisites

- Python 3.8+ installed on your system.
- `pip` and `python3-venv` installed.
- A Discord Application and Bot Token (for the frontend bot).
- (Optional) SQLite for a simple local database (default in Python).

## Setting Up the Backend (Flask API)

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations or initialize database** (if applicable):
   ```bash
   # Example command if you have a migration script
   # flask db upgrade
   # Otherwise, ensure your models create the DB tables on first run
   ```

5. **Start the Flask server**:
   ```bash
   flask run
   ```
   By default, the backend will run at `http://127.0.0.1:5000`.

   **Testing an Endpoint**:
   ```bash
   curl -X GET http://127.0.0.1:5000/api/user/some_discord_id
   ```

## Setting Up the Discord Bot (Frontend)

1. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Discord token**:
   - Create a `.env` file in the `frontend/` directory:
     ```bash
     echo "DISCORD_TOKEN=your_discord_bot_token_here" > .env
     ```
   
   Replace `your_discord_bot_token_here` with the token from the Discord Developer Portal.

5. **Run the bot**:
   ```bash
   python bot.py
   ```

   If the bot starts successfully, you should see a message like:
   ```
   Logged in as <bot_name>
   ```

6. **Invite the Bot to Your Server**:
   - In the Discord Developer Portal, generate an OAuth2 URL with the `bot` scope and needed permissions.
   - Open that URL in your browser, select your test server, and authorize the bot.
   - In Discord, type `!ping` in a channel the bot has access to. It should respond with `Pong!`.

## Using the Text Client (for Testing the Backend)

1. **Navigate to the text-client directory**:
   ```bash
   cd ../text-client
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Test an Endpoint**:
   - Ensure the backend is running.
   - Run a test command (for example, listing tasks for a user):
     ```bash
     python client.py list_tasks 123456789
     ```
   
   You should see a JSON response printed out, confirming that the backend is reachable.

## Common Troubleshooting

- **Backend 404 Errors**:  
  Ensure the blueprint routes are correctly registered, and the server is running on the expected port. Confirm you’re using the correct endpoint URLs.

- **Bot Not Responding to Commands**:  
  Check that you’ve enabled the `message_content` intent in the Developer Portal and in your code. Confirm the bot has permission to send messages in the channel.

- **Text Client Errors**:  
  Double-check the `BASE_URL` in `client.py` and ensure the backend is running. Confirm correct user IDs or parameters when running commands.

## Future Enhancements

- Add more detailed environment variable management (like using `python-dotenv` in the backend).
- Implement database migrations and a structured deployment process.
- Provide a Dockerfile or docker-compose setup for easier deployment.
