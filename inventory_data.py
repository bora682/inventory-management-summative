# inventory_data.py

# Our in-memory "database" – just a list of dicts for now.
inventory = [
    {
        "id": 1,
        "barcode": "1234567890123",
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds, cane sugar, sea salt",
        "price": 4.99,
        "stock": 10,
    },
    {
        "id": 2,
        "barcode": "9876543210987",
        "name": "Greek Yogurt",
        "brand": "Chobani",
        "ingredients": "Cultured pasteurized nonfat milk, live and active cultures",
        "price": 1.59,
        "stock": 25,
    },
]

# Simple ID counter – every new item increments this
next_id = 3


def get_all_items():
    """Return the full inventory list."""
    return inventory


def get_item_by_id(item_id: int):
    """Return a single item dict by id, or None if not found."""
    return next((item for item in inventory if item["id"] == item_id), None)


def add_item(data: dict):
    """Add a new item to the inventory and return it."""
    global next_id

    new_item = {
        "id": next_id,
        "barcode": data.get("barcode"),
        "name": data.get("name"),
        "brand": data.get("brand"),
        "ingredients": data.get("ingredients"),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
    }

    inventory.append(new_item)
    next_id += 1
    return new_item


def update_item(item_id: int, updates: dict):
    """
    Update an existing item with partial data.
    Returns the updated item, or None if not found.
    """
    item = get_item_by_id(item_id)
    if not item:
        return None

    # Only update keys that already exist on the item
    for key, value in updates.items():
        if key in item and key != "id":  # never modify id
            item[key] = value

    return item


def delete_item(item_id: int):
    """
    Delete an item by id.
    Returns True if something was deleted, False otherwise.
    """
    global inventory
    before = len(inventory)
    inventory = [item for item in inventory if item["id"] != item_id]
    return len(inventory) < before
