from flask import Flask, jsonify, request

from inventory_data import (
    get_all_items,
    get_item_by_id,
    add_item,
    update_item,
    delete_item,
)

from external_api import fetch_product_by_barcode

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


# POST /inventory/from-barcode -> create a new item using OpenFoodFacts
@app.route("/inventory/from-barcode", methods=["POST"])
def create_item_from_barcode():
    """
    Create a new inventory item by looking up details from OpenFoodFacts
    using a barcode, and combining that with local price/stock from the client.
    Expected JSON body:
        {
            "barcode": "737628064502",
            "price": 4.99,
            "stock": 10
        }
    """
    data = request.get_json() or {}

    barcode = data.get("barcode")
    if not barcode:
        return jsonify({"error": "barcode is required"}), 400

    # Call our helper to fetch product info from OpenFoodFacts
    product_info = fetch_product_by_barcode(barcode)
    if not product_info:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404

    # Combine API data with local price/stock (or defaults)
    item_data = {
        "barcode": product_info["barcode"],
        "name": product_info["name"],
        "brand": product_info["brand"],
        "ingredients": product_info["ingredients"],
        "price": float(data.get("price", 0.0)),
        "stock": int(data.get("stock", 0)),
    }

    new_item = add_item(item_data)
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
