from flask import Flask , jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db
import os

app = Flask(__name__)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate = Migrate(app, db)
@app.route("/")
def index():
    return jsonify({"message" : "Your Workout app is running"})

if __name__ == "__main__":
    app.run(debug=True , port=5000)