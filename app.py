from flask import Flask , jsonify , request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Workout, Exercise, WorkoutExercise
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

# create workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    workout = Workout(
        title=data.get("title"),
        description=data.get("description")
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify({"message": "Workout created", "id": workout.id}), 201

# get all workout
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    result = []
    for w in workouts:
        result.append({
            "id": w.id,
            "title": w.title,
            "description": w.description
        })

    return jsonify(result)

# get one workout
@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)

    exercises = []
    for we in workout.workout_exercises:
        exercises.append({
            "exercise_id": we.exercise.id,
            "name": we.exercise.name,
            "sets": we.sets,
            "reps": we.reps,
            "duration": we.duration
        })

    return jsonify({
        "id": workout.id,
        "title": workout.title,
        "description": workout.description,
        "exercises": exercises
    })
# delete workout 
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted"})

# create exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    exercise = Exercise(
        name=data.get("name"),
        muscle_group=data.get("muscle_group"),
        equipment=data.get("equipment")
    )

    db.session.add(exercise)
    db.session.commit()

    return jsonify({"message": "Exercise created", "id": exercise.id}), 201


# get all exercises
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    result = []
    for e in exercises:
        result.append({
            "id": e.id,
            "name": e.name,
            "muscle_group": e.muscle_group,
            "equipment": e.equipment
        })

    return jsonify(result)

# get one exercise 
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    e = Exercise.query.get_or_404(id)

    return jsonify({
        "id": e.id,
        "name": e.name,
        "muscle_group": e.muscle_group,
        "equipment": e.equipment
    })





if __name__ == "__main__":
    app.run(debug=True , port=5000)