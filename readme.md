https://realpython.com/flask-connexion-rest-api/
https://realpython.com/flask-connexion-rest-api-part-2/
https://realpython.com/flask-connexion-rest-api-part-3/#handle-notes-with-your-rest-api


python -m pip install Flask==2.2.2
python -m pip install "connexion[swagger-ui]==2.14.1"
python -m pip install "flask-marshmallow[sqlalchemy]==0.14.0

<!-- The OpenAPI Specification is an API description format for REST APIs and provides a lot of functionality, including
Validation of input and output data to and from your API
Configuration of the API URL endpoints and the expected parameters -->
1. Define API endpoints using the OpenAPI specification in a config file
The Connexion module allows a Python program 
2. to use the OpenAPI specified config to handle HTTP requests i.e. to create actual end points as well as to 
3. Build API documentation with Swagger UI
4. Configure a SQLite database for your Flask project
5. Use SQLAlchemy to save Python objects to your database or as an interface to interact between flask and the underlying database
6. Leverage the Marshmallow library to serialize(Python Instance to JSON) and deserialize(JSON to Instance) data
7. Connect your REST API with your database through read, read_one, create, update and delete functions.


Testing:
https://ericbernier.com/flask-restful-api

pip install Flask-Testing pytest


-- Recommended API project structure

fantasy_stats/
│
├── football_api/
│   ├── __init__.py
│   ├── api.py
│   ├── constants.py
│   ├── database.py
│   └── models/
|       └── __init__.py
│   └── resources/
|       └── __init__.py
│   └── schemas/
|       └── __init__.py
├── tests/
|   └── integration/
├── Pipfile
├── Pipfile.lock
└── fantasy_football.db <--- We will download this file below.


https://testdriven.io/blog/flask-contexts/
https://ericbernier.com/flask-restful-api
https://testdriven.io/blog/flask-pytest/


--------------------------

ou specify your configurations in config.py like so:

class Dev(Config):
    DEBUG = True
    MAIL_DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/%s_dev.sqlite" % project_name
This inherits the Config class which can contain your defaults. From there, main.py has methods for creating a flask instance from the config.py file, manage.py determines which config is loaded.

Here's a snippet from main.py so you get the idea:

def app_factory(config, app_name=None, blueprints=None):
    app_name = app_name or __name__
    app = Flask(app_name)

    config = config_str_to_obj(config)
    configure_app(app, config)
    configure_blueprints(app, blueprints or config.BLUEPRINTS)
    configure_error_handlers(app)
    configure_database(app)
    configure_views(app)

    return app

    https://gitlab.com/patkennedy79/flask_user_management_example/-/blob/main/tests/conftest.py

    -------------------------------------------------------------

The client sends a login request with their credentials to the server.
If the credentials are valid, the server generates a JWT and sends it back to the client.
The client stores the JWT and includes it in the header of all subsequent requests to the server.
The server verifies the JWT on each request to ensure that the client is authenticated and authorized to access the requested resources.

JWTs consist of three parts: a header, a payload, and a signature.

The header contains information about the type of token and the signature algorithm used to generate it.
The payload contains the claims, which are statements about an entity (typically, the user) and the actions that can be performed on the API.
The signature is used to verify that the sender of the JWT is who it says it is and to ensure that the message hasn’t been tampered with.



- autherization, basic, bearer apikey Headers -> (Autherization: username_or_token:password, X-API-Key: abcdef12345)
- logging
- rate-limiting
What is Rate Limiting?
Rate Limiting allows you to control how often someone can access your API in a given time period. In flask there is a extension called flask limiter. This extension allows you to limit the amount of request on a particular route.
flask-limiter
https://medium.com/analytics-vidhya/how-to-rate-limit-routes-in-flask-61c6c791961b
https://stackoverflow.com/questions/67835964/rate-limit-rest-api-made-with-connexion-and-swagger
https://resources.socie.nl/docs/api/ui/index.html
- api-versioning (Accepts-version: 1.0)



@pytest.fixture()
def generate_api_key():
    """
    generate_test_password
        A fixture to generate strong test password
    """
    characters = string.ascii_letters + string.punctuation + string.digits
    return "".join(choice(characters) for _ in range(randint(8, 16)))


https://ericbernier.com/flask-restful-api
https://testdriven.io/blog/flask-contexts/
https://gitlab.com/patkennedy79/flask_user_management_example/-/tree/main
https://realpython.com/token-based-authentication-with-flask/#jwt-setup
https://github.com/miguelgrinberg/REST-auth/blob/2904b70ea95885bc523e472e58e934925f1ab1eb/api.py#L5




http://127.0.0.1:8000/api/peope
http://127.0.0.1:8000/api/ui/