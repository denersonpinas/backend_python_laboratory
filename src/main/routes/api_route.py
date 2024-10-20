from flask import Blueprint, jsonify, request
from src.main.adapter.api_adapter import flask_adapter
from src.main.composer import register_user_composer

api_routes_bp = Blueprint("api_routes", __name__)


@api_routes_bp.route("/api", methods=["GET"])
def something():
    """teste"""

    return jsonify({"Programador": "dennerpinas"})


@api_routes_bp.route("/api/users", methods=["POST"])
def register_user():
    """register user route"""

    message = {}
    response = flask_adapter(request=request, api_route=register_user_composer())

    if response.status_code < 300:
        message = {
            "Type": "users",
            "id": response.body.id,
            "attributest": {"name": response.body.name},
        }

        return jsonify({"Data": message}), response.status_code

    # Handling Errors
    return (
        jsonify(
            {"error": {"status": response.status_code, "title": response.body["error"]}}
        ),
        response.status_code,
    )
