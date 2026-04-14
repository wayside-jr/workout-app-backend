from marshmallow import Schema, fields, validate ,ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    muscle_group = fields.Str(required=True)
    equipment = fields.Str(allow_none=True)



class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)

    sets = fields.Int(required=True, validate=validate.Range(min=1))
    reps = fields.Int(required=True, validate=validate.Range(min=1))



class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str()

    # nested exercises inside workout
    exercises = fields.List(fields.Nested(WorkoutExerciseSchema))