# Workout Tracker API

## Project Description

This is a Flask REST API for a workout tracking application. The API allows users to create and manage workouts and exercises, and assign exercises to workouts. Each workout can contain multiple exercises with associated sets and reps.

The application uses Flask, SQLAlchemy, and Marshmallow to manage database models, relationships, validation, and serialization.



## How the Application Works

The system is built around three main models:

- Workout
- Exercise
- WorkoutExercise (linking table)


### Workflow

1. Create an Exercise first (e.g. Squats, Push Ups)
2. Create a Workout (e.g. Chest Day, Leg Day)
3. Link an Exercise to a Workout using WorkoutExercise
4. Retrieve workouts to view all assigned exercises with their training details

---

## Technologies Used

- Python 3.12+
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Marshmallow
- SQLite

## author
Jeremy Junior

## licence
MIT