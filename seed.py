from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():

  
    print("Clearing old data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    
    print("Creating workouts...")

    leg_day = Workout(
        title="Leg Day",
        description="Lower body strength workout"
    )

    push_day = Workout(
        title="Push Day",
        description="Chest, shoulders and triceps workout"
    )

    db.session.add_all([leg_day, push_day])
    db.session.commit()


    print("Creating exercises...")

    squats = Exercise(
        name="Squats",
        muscle_group="Legs",
        equipment="Barbell"
    )

    pushups = Exercise(
        name="Push Ups",
        muscle_group="Chest",
        equipment=None
    )

    plank = Exercise(
        name="Plank",
        muscle_group="Core",
        equipment=None
    )

    db.session.add_all([squats, pushups, plank])
    db.session.commit()

   
    print("Linking workouts and exercises...")

    we1 = WorkoutExercise(
        workout_id=leg_day.id,
        exercise_id=squats.id,
        sets=4,
        reps=12
    )

    we2 = WorkoutExercise(
        workout_id=push_day.id,
        exercise_id=pushups.id,
        sets=3,
        reps=15
    )

    we3 = WorkoutExercise(
        workout_id=push_day.id,
        exercise_id=plank.id,
        sets=3,
        reps=60 
    )

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeded successfully!")