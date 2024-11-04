from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Create the engine and metadata globally
DATABASE_URL = 'sqlite:///example.db'  # Change this URL if you're using another database
engine = create_engine(DATABASE_URL)

metadata = MetaData()

# Define a SessionLocal class for session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    global engine
    """Return the SQLAlchemy engine for global use."""
    return engine

def get_session():
    """Return a new session instance."""
    return SessionLocal()
