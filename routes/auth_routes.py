from flask import Blueprint, request, jsonify
from services.auth_service import signup_service, login_service

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():

    response, status = signup_service(request.json)

    return jsonify(response), status


@auth_bp.route("/login", methods=["POST"])
def login():

    response, status = login_service(request.json)

    return jsonify(response), status