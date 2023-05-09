from flask import abort, g, jsonify
from people_api.config import db
from people_api.models import User, user_schema


def verify_password(username_or_token, password=None):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            abort(401, "Unauthorized request.")
    g.user = user
    return {"id": user.id}


def get_auth_token():
    if "user" in g:
        token = g.user.generate_auth_token()
        return jsonify({'token': token, 'duration': 600})
    else:
        abort(401, "Unauthorized request.")

def create(user):
    print("Fatima")
    print(user)
    username = user.get('username')
    password = user.get('password')
    if username is None or password is None:
        abort(400, f"Missing username or password.")    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(406, f"User with username {username} already exists")    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201


def read_one(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, "User does not exist.")
    return user_schema.dump(user), 200