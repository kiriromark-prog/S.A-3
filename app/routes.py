from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Workout, Exercise, WorkoutExercise
from app.schemas import (workout_schema, workouts_schema, exercise_schema, 
                         exercises_schema, exercise_detail_schema, workout_exercise_schema)
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

api_bp = Blueprint('api', __name__)

@api_bp.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200

@api_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify(workout_schema.dump(workout)), 200

@api_bp.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
        new_workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify(workout_schema.dump(new_workout)), 201
    except ValidationError as err:
        return jsonify({"schema_errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"validation_error": str(err)}), 400

@api_bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout ID {id} purged completely."}), 200

@api_bp.route('/exercises', methods=['GET'])
def get_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200

@api_bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return jsonify(exercise_detail_schema.dump(exercise)), 200

@api_bp.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201
    except ValidationError as err:
        return jsonify({"schema_errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"validation_error": str(err)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"database_error": "An exercise with this name already exists."}), 400

@api_bp.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise '{exercise.name}' dropped successfully."}), 200

@api_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    try:
        data = workout_exercise_schema.load(request.get_json() or {})
        association = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(association)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except ValidationError as err:
        return jsonify({"schema_errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"validation_error": str(err)}), 400
