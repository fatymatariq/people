import pytest
import base64
from people_api import config
from people_api.constants import TOKEN_ENDPOINT
from people_api.models import User

USERNAME = 'test'
PASSWORD = 'FlaskIsAwesome'


@pytest.fixture(scope='module')
def client(request, tmp_path_factory):
    temp_db = f"sqlite:///{tmp_path_factory.mktemp('data').joinpath('people.db')}"

    connex_app = config.create_app(temp_db)
    app = connex_app.app
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_database()

    def teardown():
        with app.app_context():
            tear_database()

    request.addfinalizer(teardown)

    yield client


@pytest.fixture(scope='module')
def token_header(client):
    auth_string = f"{USERNAME}:{PASSWORD}"
    encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    headers = {"Authorization": f"Basic {encoded_auth_string}"}
    response = client.get(TOKEN_ENDPOINT, headers=headers)
    return {"Authorization": f"Bearer {response.json['token']}"}


def init_database():
    config.db.create_all()

    user = User(username=USERNAME)
    user.hash_password(PASSWORD)
    config.db.session.add(user)

    config.db.session.commit()


def tear_database():
    config.db.session.remove()
    config.db.drop_all()



