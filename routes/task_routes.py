from flask import Blueprint, request, jsonify
from middleware.jwt_middleware import token_required
from services.task_service import (
    add_task_service,
    get_tasks_service,
    update_task_service,
    patch_status_service,
    delete_task_service
)

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/", methods=["POST"])
@token_required
def add_task():

    response, status = add_task_service(
        request.json,
        request.user_id
    )

    return jsonify(response), status


@task_bp.route("/", methods=["GET"])
@token_required
def get_tasks():

    response = get_tasks_service(request.user_id)

    return jsonify(response), 200


@task_bp.route("/<int:task_id>", methods=["PUT"])
@token_required
def update_task(task_id):

    response, status = update_task_service(
        task_id,
        request.json,
        request.user_id
    )

    return jsonify(response), status


@task_bp.route("/<int:task_id>/status", methods=["PATCH"])
@token_required
def patch_status(task_id):

    response, status = patch_status_service(
        task_id,
        request.json,
        request.user_id
    )

    return jsonify(response), status


@task_bp.route("/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(task_id):

    response, status = delete_task_service(
        task_id,
        request.user_id
    )

    return jsonify(response), status