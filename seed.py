from app import create_app
from app.database import db
from app.models import Workout, Exercise, WorkoutExercise
from datetime import date

app = create_app()

def run_seed():
    with app.app_context():
        print("Clearing tables...")
        db.session.query(WorkoutExercise).delete()
        db.session.query(Workout).delete()
        db.session.query(Exercise).delete()
        db.session.commit()

        print("Seeding Exercises...")
        ex1 = Exercise(name="Pushups", category="Calisthenics", equipment_needed=False)
        ex2 = Exercise(name="Deadlift", category="Powerlifting", equipment_needed=True)
        db.session.add_all([ex1, ex2])
        db.session.commit()

        print("Seeding Workouts...")
        w1 = Workout(date=date(2026, 7, 27), duration_minutes=45, notes="Afternoon lifting loop")
        db.session.add(w1)
        db.session.commit()

        print("Mapping relations data...")
        map_record = WorkoutExercise(workout=w1, exercise=ex2, reps=5, sets=3)
        db.session.add(map_record)
        db.session.commit()
        print("Database cleanly loaded!")

if __name__ == '__main__':
    run_seed()
