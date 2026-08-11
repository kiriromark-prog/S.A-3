# STK Workout Spec Tracker

A lightweight Flask API for tracking workouts, exercises, and workout/exercise relationships.

## Project Overview

This project provides a simple REST API for:  
- managing workouts  
- managing exercises  
- associating exercises with workouts and tracking reps/sets/duration  

It uses Flask, Flask-SQLAlchemy, and Marshmallow for validation and serialization.

## Requirements

- Python 3.11+ (or a compatible Python 3 environment)
- `requirements.txt` dependencies:
  - Flask==3.0.3
  - Flask-SQLAlchemy==3.1.1
  - marshmallow==3.21.3

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Start the application from the project root:

```bash
python run.py
```

By default, the Flask development server runs with `debug=True`.

## Database

The app uses SQLite and stores data in `workout_spec_tracker.db` at the project root.

Database tables are created automatically when the app starts.

## Seeding Sample Data

Populate the database with example data using:

```bash
python seed.py
```

This script clears existing data and inserts sample exercises, a workout, and a workout/exercise mapping.

## API Endpoints

### Workouts

- `GET /workouts`
  - List all workouts.
- `GET /workouts/<id>`
  - Retrieve a workout by ID.
- `POST /workouts`
  - Create a workout.
  - JSON body example:

```json
{
  "date": "2026-08-11",
  "duration_minutes": 60,
  "notes": "Morning session"
}
```
- `DELETE /workouts/<id>`
  - Delete a workout by ID.

### Exercises

- `GET /exercises`
  - List all exercises.
- `GET /exercises/<id>`
  - Retrieve exercise details by ID.
- `POST /exercises`
  - Create an exercise.
  - JSON body example:

```json
{
  "name": "Bench Press",
  "category": "Strength",
  "equipment_needed": true
}
```
- `DELETE /exercises/<id>`
  - Delete an exercise by ID.

### Workout-Exercise Mapping

- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`
  - Add an exercise to a workout.
  - JSON body example:

```json
{
  "reps": 8,
  "sets": 3,
  "duration_seconds": 120
}
```

## Data Models

- `Workout`
  - `id`, `date`, `duration_minutes`, `notes`
  - Related exercises via `workout_exercises`
- `Exercise`
  - `id`, `name`, `category`, `equipment_needed`
- `WorkoutExercise`
  - Join model for workout/exercise associations
  - Tracks `reps`, `sets`, and `duration_seconds`

## Notes

- Validation is handled with Marshmallow schemas and model validators.
- The API returns JSON responses and HTTP status codes for success and validation errors.

## License

This project does not currently include a license file.
