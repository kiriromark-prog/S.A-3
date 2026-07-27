from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    """Structural schemas matching business rules gate criteria"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[
        validate.Length(min=2, max=100, error="Name must be between 2 and 100 characters long."),
        validate.NoneOf(["", " "], error="Name cannot be spaces.")
    ])
    category = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseSchema(Schema):
    """Validates parameters sent onto the intermediary join mapping table"""
    reps = fields.Int(allow_none=True, validate=validate.Range(min=0, error="Reps cannot be a negative value."))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=0, error="Sets cannot be a negative value."))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=0, error="Duration seconds cannot be negative."))


class WorkoutExerciseNestedOutputSchema(WorkoutExerciseSchema):
    """Outputs join data metrics along side child schema descriptions"""
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    """Handles serialization and formatting arrays tracking metrics"""
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, error_messages={"invalid": "Supply standard validation formatting YYYY-MM-DD."})
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=480))
    notes = fields.Str(allow_none=True)
    
    # Nesting details setup satisfying your stretch objective layout metrics
    exercises = fields.Nested(
        WorkoutExerciseNestedOutputSchema, 
        attribute='workout_exercises', 
        many=True, 
        dump_only=True
    )

class WorkoutExerciseNestedInExerciseSchema(WorkoutExerciseSchema):
    workout = fields.Nested(WorkoutSchema, exclude=('exercises',), dump_only=True)

class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.Nested(
        WorkoutExerciseNestedInExerciseSchema, 
        attribute='workout_exercises', 
        many=True, 
        dump_only=True
    )

# Instantiate schemas
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()
