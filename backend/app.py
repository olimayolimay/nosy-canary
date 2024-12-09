from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Task, Intention  # db comes from models now

import logging
from logging.handlers import RotatingFileHandler

# import and configure app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

# Configure Logging
def setup_logging(app):
    """
    Sets up logging for the Flask application.
    Logs ERROR and above messages to a rotating log file.
    """
    # Create a RotatingFileHandler
    handler = RotatingFileHandler('error.log', maxBytes=100000, backupCount=3)
    handler.setLevel(logging.ERROR)  # Log only ERROR and above levels

    # Define log message format
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)

    # Add the handler to the app's logger
    app.logger.addHandler(handler)

# Call the logging setup function
setup_logging(app)

# create tables
with app.app_context():
    db.create_all()

# import and register blueprints

from routes.user_routes import user_bp
app.register_blueprint(user_bp)

from routes.tasks import bp as tasks_bp
app.register_blueprint(tasks_bp)

from routes.intentions import bp as intentions_bp
app.register_blueprint(intentions_bp)

from routes.timer import timer_bp
app.register_blueprint(timer_bp)

# define routes

@app.route('/')
def hello():
    return "Nosy Canary Backend is Running!"

# scheduler
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

def scheduled_job():
    # In a real scenario, you might update a database value, log a message, or enqueue a bot action.
    # For now, just log to confirm it runs.
    app.logger.info("Scheduled job ran!")

# Add the job to run every hour:
scheduler.add_job(scheduled_job, 'interval', minutes=1)  # Changed to minutes=1 for testing

# run app if main script
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
