from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Task, Intention  # db comes from models now

# import and configure app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

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

# define routes

@app.route('/')
def hello():
    return "Nosy Canary Backend is Running!"

# run app if main script
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

