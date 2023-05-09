import pathlib

# Path to the current working directory
BASE_DIR = pathlib.Path(__file__).parent.resolve()

PEOPLE_DATABASE_NAME = "people.db"

PEOPLE_DATABASE_URI = f"sqlite:///{BASE_DIR / PEOPLE_DATABASE_NAME}"

API_CONFIG_FILE = "swagger.yml"

NOTES_ENDPOINT = "api/notes"

PEOPLE_ENDPOINT = "api/people"

USERS_ENDPOINT = "api/users"

TOKEN_ENDPOINT = f"{USERS_ENDPOINT}/token"