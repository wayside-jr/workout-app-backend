from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from models import db, Workout, Exercise, WorkoutExercise
from schema import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =====================
# CONFIG
# =====================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# =====================
# SCHEMAS
# =====================
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

# =====================
# ERROR HANDLER (VALIDATION)
# =====================
@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({
        "errors": err.messages
    }), 400


# =====================
# HOME
# =====================
@app.route("/")
def index():
    return jsonify({"message": "Your Workout app is running"})


# =====================
# WORKOUT ROUTES
# =====================

# CREATE WORKOUT (WITH VALIDATION)
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    validated_data = workout_schema.load(data)

    workout = Workout(
        title=validated_data["title"],
        description=validated_data.get("description")
    )

    db.session.add(workout)
    db.session.commit()

    return workout_schema.dump(workout), 201


# GET ALL WORKOUTS
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200


# GET SINGLE WORKOUT
@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.dump(workout), 200


# DELETE WORKOUT
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted"}), 200


# =====================
# EXERCISE ROUTES
# =====================

# CREATE EXERCISE (WITH VALIDATION)
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    validated_data = exercise_schema.load(data)

    exercise = Exercise(
        name=validated_data["name"],
        muscle_group=validated_data["muscle_group"],
        equipment=validated_data.get("equipment")
    )

    db.session.add(exercise)
    db.session.commit()

    return exercise_schema.dump(exercise), 201


# GET ALL EXERCISES
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200


# GET SINGLE EXERCISE
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.dump(exercise), 200


# DELETE EXERCISE
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "Exercise deleted"}), 200


# =====================
# LINK EXERCISE TO WORKOUT
# =====================

@app.route("/workouts/<int:workout_id>/add-exercise", methods=["POST"])
def add_exercise_to_workout(workout_id):
    data = request.get_json()

    validated_data = workout_exercise_schema.load(data)

    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(validated_data["exercise_id"])

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        sets=validated_data["sets"],
        reps=validated_data["reps"]
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return workout_exercise_schema.dump(workout_exercise), 201


# =====================
# RUN APP
# =====================
if __name__ == "__main__":
    app.run(debug=True, port=5000)