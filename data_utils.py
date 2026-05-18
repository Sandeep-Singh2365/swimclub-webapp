import os
from pathlib import Path
# try:
#     BASE_DIR = Path(__file__).resolve().parent
# except Exception:
#     BASE_DIR = Path.cwd()

from queries import *
from dbcm import UseDatabase  # our new PyMySQL DBcm


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

# This loads variables from .env file (if present).
# In production (PythonAnywhere), .env will not exist,
# so real environment variables from WSGI will be used.
from dotenv import load_dotenv
load_dotenv()

# FOLDER = BASE_DIR / "swimdata"

# ---------------------------------------------------------
# Database Configuration from environment
# ---------------------------------------------------------

def get_env_variable(name: str, required: bool = True, default=None):
    """
    Fetch environment variable safely.
    Raises a clear error if required variable is missing.
    """
    value = os.environ.get(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_db_config():
    """
    Load and validate DB configuration from environment variables.
    """
    host = get_env_variable("DB_HOST")
    database = get_env_variable("DB_NAME")
    user = get_env_variable("DB_USER")
    password = get_env_variable("DB_PASSWORD")

    # Optional port (default MySQL port 3306)
    port = get_env_variable("DB_PORT", required=False, default="3306")

    try:
        port = int(port)
    except ValueError:
        raise RuntimeError("DB_PORT must be an integer")
    
    return {
        "host": host,
        "port": int(port),
        "database": database,
        "user": user,
        "password": password
    }

db_details = load_db_config()

# ---------------------------------------------------------
# Database Functions
# ---------------------------------------------------------
def get_swim_sessions():
    """Return a tuple-list of unique session timestamps."""
    with UseDatabase(db_details) as db:
        db.execute(SQL_SESSIONS)
        return db.fetchall()

def get_session_swimmers(date):
    """When given a date (YYYY-MM-DD), return a tuple-list of swimmers
    and their associated age(filtered by date).
    """
    with UseDatabase(db_details) as db:
        db.execute(SQL_SWIMMERS_BY_SESSION, (date,))
        return db.fetchall()

def get_swimmers_events(name, age, date):
    """When given a date(YYYY-MM-DD), swimmer's name and swimmer's age,
    return a tuple-list of events the swimmer swam on that date.
    """
    with UseDatabase(db_details) as db:
        db.execute(SQL_SWIMMERS_EVENTS_BY_SESSION, (name, age, date))
        return db.fetchall()

def get_swimmers_times(name, age, distance, stroke, date):
    """When given a date(YYYY-MM-DD), swimmer's name, swimmer's age, distance and stroke
    return a tuple-list of times the swimmer swam on that date over the identified
    distance/stroke combination.
    """
    with UseDatabase(db_details) as db:
        db.execute(SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION, (name, age, distance, stroke, date))
        return db.fetchall()
