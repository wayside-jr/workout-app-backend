from flask import Flask , jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message" : "Your Workout app is running"})

if __name__ == "__main__":
    app.run(debug=True , port=5000)