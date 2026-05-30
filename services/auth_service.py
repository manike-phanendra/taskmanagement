from models.user_model import User
from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app


def signup_service(data):

    username = data.get("username")
    password = data.get("password")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"message": "User already exists"}, 400

    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "Signup successful"}, 201


def login_service(data):

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        return {"message": "Invalid username"}, 401

    if not check_password_hash(user.password, password):
        return {"message": "Invalid password"}, 401

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return {
        "token": token
    }, 200