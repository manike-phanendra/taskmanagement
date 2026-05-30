from functools import wraps
from flask import request, jsonify, current_app
import jwt


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            token = token.split(" ")[1]

            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            request.user_id = data["user_id"]

        except Exception:
            return jsonify({"message": "Invalid token"}), 401

        return func(*args, **kwargs)

    return wrapper