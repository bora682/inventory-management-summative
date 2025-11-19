from flask import Flask, jsonify, request

from inventory_data import (
    get_all_items,
    get_item_by_id,
    add_item,
    update_item,
    delete_item,
)

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Inventory API running!"}), 200


# ---------- CRUD ROUTES ----------

# GET /inventory -> list all items
@app.route("/inventory", methods=["GET"])
def list_inventory():
    items = get_all_items()
    return jsonify(items), 200


# GET /inventory/<id> -> get one item by id
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


# POST /inventory -> create a new item
@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json() or {}

    # basic validation: require at least name, price, stock
    required_fields = ["name", "price", "stock"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "missing_fields": missing,
                }
            ),
            400,
        )

    new_item = add_item(data)
    return jsonify(new_item), 201


# PATCH /inventory/<id> -> update an item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_inventory_item(item_id):
    data = request.get_json() or {}
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    updated = update_item(item_id, data)
    if updated is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(updated), 200


# DELETE /inventory/<id> -> delete an item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    deleted = delete_item(item_id)
    if not deleted:
        return jsonify({"error": "Item not found"}), 404

    # No body for 204
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
