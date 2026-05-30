from flasgger import Swagger
from flask import Flask, render_template

from config.database import init_db
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "supersecretkey"
app.config["SWAGGER"] = {
    "title": "Task Management",
    "uiversion": 3
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Task Management",
        "description": "Authentication and task management API",
        "version": "1.0.0"
    },
    "basePath": "/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter JWT as: Bearer <token>"
        }
    },
    "definitions": {
        "AuthCredentials": {
            "type": "object",
            "required": ["username", "password"],
            "properties": {
                "username": {"type": "string", "example": "gopika"},
                "password": {"type": "string", "example": "password123"}
            }
        },
        "TaskInput": {
            "type": "object",
            "required": ["title"],
            "properties": {
                "title": {"type": "string", "example": "Finish report"},
                "description": {
                    "type": "string",
                    "example": "Complete the weekly status report"
                },
                "status": {"type": "string", "example": "pending"}
            }
        },
        "TaskStatusInput": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"type": "string", "example": "completed"}
            }
        },
        "Task": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "title": {"type": "string", "example": "Finish report"},
                "description": {
                    "type": "string",
                    "example": "Complete the weekly status report"
                },
                "status": {"type": "string", "example": "pending"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            }
        },
        "TaskResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "task": {"$ref": "#/definitions/Task"}
            }
        },
        "MessageResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        }
    },
    "paths": {
        "/api/auth/signup": {
            "post": {
                "tags": ["Auth"],
                "summary": "Create a user account",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/AuthCredentials"}
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Signup successful",
                        "schema": {"$ref": "#/definitions/MessageResponse"}
                    },
                    "400": {"description": "User already exists"}
                }
            }
        },
        "/api/auth/login": {
            "post": {
                "tags": ["Auth"],
                "summary": "Log in and receive a JWT",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/AuthCredentials"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "token": {"type": "string"}
                            }
                        }
                    },
                    "401": {"description": "Invalid username or password"}
                }
            }
        },
        "/api/tasks/": {
            "get": {
                "tags": ["Tasks"],
                "summary": "Get all tasks for the authenticated user",
                "security": [{"Bearer": []}],
                "responses": {
                    "200": {
                        "description": "List of tasks",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/Task"}
                        }
                    },
                    "401": {"description": "Missing or invalid token"}
                }
            },
            "post": {
                "tags": ["Tasks"],
                "summary": "Create a task",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/TaskInput"}
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Task created",
                        "schema": {"$ref": "#/definitions/TaskResponse"}
                    },
                    "400": {"description": "Title is required"},
                    "401": {"description": "Missing or invalid token"}
                }
            }
        },
        "/api/tasks/{task_id}": {
            "put": {
                "tags": ["Tasks"],
                "summary": "Update a task",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/TaskInput"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Task updated",
                        "schema": {"$ref": "#/definitions/TaskResponse"}
                    },
                    "400": {"description": "Title is required"},
                    "401": {"description": "Missing or invalid token"},
                    "404": {"description": "Task not found"}
                }
            },
            "delete": {
                "tags": ["Tasks"],
                "summary": "Delete a task",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Task deleted",
                        "schema": {"$ref": "#/definitions/MessageResponse"}
                    },
                    "401": {"description": "Missing or invalid token"},
                    "404": {"description": "Task not found"}
                }
            }
        },
        "/api/tasks/{task_id}/status": {
            "patch": {
                "tags": ["Tasks"],
                "summary": "Update task status",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/TaskStatusInput"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Task status updated",
                        "schema": {"$ref": "#/definitions/TaskResponse"}
                    },
                    "400": {"description": "Status is required"},
                    "401": {"description": "Missing or invalid token"},
                    "404": {"description": "Task not found"}
                }
            }
        }
    }
}

Swagger(app, template=swagger_template)

init_db(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(task_bp, url_prefix="/api/tasks")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
