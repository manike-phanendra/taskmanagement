from models.task_model import Task
from config.database import db


def _task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


def add_task_service(data, user_id):
    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "pending")

    if not title:
        return {"message": "Title is required"}, 400

    task = Task(
        title=title,
        description=description,
        status=status,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return {
        "message": "Task created successfully",
        "task": _task_to_dict(task)
    }, 201


def get_tasks_service(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()

    return [_task_to_dict(task) for task in tasks]


def update_task_service(task_id, data, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return {"message": "Task not found"}, 404

    title = data.get("title")

    if not title:
        return {"message": "Title is required"}, 400

    task.title = title
    task.description = data.get("description")
    task.status = data.get("status", task.status)

    db.session.commit()

    return {
        "message": "Task updated successfully",
        "task": _task_to_dict(task)
    }, 200


def patch_status_service(task_id, data, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return {"message": "Task not found"}, 404

    status = data.get("status")

    if not status:
        return {"message": "Status is required"}, 400

    task.status = status
    db.session.commit()

    return {
        "message": "Task status updated successfully",
        "task": _task_to_dict(task)
    }, 200


def delete_task_service(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return {"message": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return {"message": "Task deleted successfully"}, 200
