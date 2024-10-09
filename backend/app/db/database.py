from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database URL
DATABASE_URL = "sqlite:///./database.db"

# Create a new database engine and configured Session class
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Create a base class for models
Base = declarative_base()

# Create the database tables
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def list_tables():
    inspector = inspect(engine)  # Create an inspector object
    tables = inspector.get_table_names()  # Get the list of tables
    return tables


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()