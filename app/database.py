from flask_sqlalchemy import SQLAlchemy

# Shared DB engine reference to avoid complex circular importing loops
db = SQLAlchemy()
