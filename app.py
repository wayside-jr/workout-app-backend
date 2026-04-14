from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Workout, Exercise, WorkoutExercise
from schema import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)

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
# ERROR HANDLING
# =====================
@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"errors": err.messages}), 400


# =====================
# HOME
# =====================
@app.route("/")
def index():
    return jsonify({"message": "Workout API running"})


# =====================
# WORKOUTS
# =====================

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    validated = workout_schema.load(data)

    workout = Workout(
        title=validated["title"],
        description=validated.get("description")
    )

    db.session.add(workout)
    db.session.commit()

    return workout_schema.dump(workout), 201


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.dump(workout), 200


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted"}), 200


# =====================
# EXERCISES
# =====================

@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    validated = exercise_schema.load(data)

    # FIX: prevent duplicate crash
    existing = Exercise.query.filter_by(name=validated["name"]).first()
    if existing:
        return jsonify({"error": "Exercise already exists"}), 400

    exercise = Exercise(
        name=validated["name"],
        muscle_group=validated["muscle_group"],
        equipment=validated.get("equipment")
    )

    db.session.add(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 400

    return exercise_schema.dump(exercise), 201


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.dump(exercise), 200


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
    validated = workout_exercise_schema.load(data)

    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(validated["exercise_id"])

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        sets=validated["sets"],
        reps=validated["reps"]
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return workout_exercise_schema.dump(workout_exercise), 201


# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(debug=True, port=5000)