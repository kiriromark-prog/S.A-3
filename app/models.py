from app.database import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

class Exercise(db.Model):
    """Exercise Model"""
    __tablename__ = 'exercises'
    
    # --- Table Constraints ---
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade="all, delete-orphan")
    workouts = association_proxy('workout_exercises', 'workout')

    # --- Model Validations ---
    @validates('name', 'category')
    def validate_strings(self, key, value):
        if not value or not str(value).strip():
            raise ValueError(f"Exercise property '{key}' cannot evaluate to empty space strings.")
        return str(value).strip()


class Workout(db.Model):
    """Workout Model"""
    __tablename__ = 'workouts'
    
    # --- Table Constraints ---
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade="all, delete-orphan")
    exercises = association_proxy('workout_exercises', 'exercise')

    # --- Model Validations ---
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is not None and (value <= 0 or value > 480):
            raise ValueError("Workout session duration must be a positive integer between 1 and 480 minutes.")
        return value


class WorkoutExercise(db.Model):
    """WorkoutExercises Join Table Model"""
    __tablename__ = 'workout_exercises'
    
    # --- Table Constraints ---
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    # Relationship maps back to explicit parents
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # --- Model Validations ---
    @validates('reps', 'sets', 'duration_seconds')
    def validate_performance_metrics(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"Tracking metric '{key}' cannot be configured below zero.")
        return value
