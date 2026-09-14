from flask import Flask, request, jsonify
from flask_cors import CORS
from crud import (
    init_db,
    get_items,
    add_item,
    delete_item,
    register_user,
    login_user
)
app = Flask(__name__)
CORS(app)

db = init_db()


@app.route("/")
def home():
    return jsonify({
        "message": "Flask App is running!"
    })


@app.route("/items", methods=["GET"])
def read_items():
    return jsonify(get_items(db))


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "error": "name is required"
        }), 400

    return jsonify(add_item(db, data)), 201

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({
            "error": "username and password are required"
        }), 400

    result = register_user(
        db,
        data["username"],
        data["password"]
    )

    if "error" in result:
        return jsonify(result), 409

    return jsonify(result), 201
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({
            "error": "username and password are required"
        }), 400

    result = login_user(
        db,
        data["username"],
        data["password"]
    )

    if "error" in result:
        return jsonify(result), 401

    return jsonify(result), 200
@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item_route(item_id):
    return jsonify(delete_item(db, item_id))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )