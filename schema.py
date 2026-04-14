from marshmallow import Schema, fields, validate, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    muscle_group = fields.Str(required=True)
    equipment = fields.Str(required=False, allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)

    sets = fields.Int(required=True, validate=validate.Range(min=1))
    reps = fields.Int(required=True, validate=validate.Range(min=1))


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str()

    exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema),
        dump_only=True
    )