from flask import Flask , jsonify
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app)

@app.route("/")
def index():
    return jsonify({"message" : "Your Workout app is running"})

if __name__ == "__main__":
    app.run(debug=True , port=5000)