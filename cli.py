# cli.py

"""
A simple command-line interface for interacting with the inventory system.
This is not part of the Flask server — it's a separate tool the user can run
to manually view or add items in the inventory.
"""

from inventory_data import (
    get_all_items,
    get_item_by_id,
    add_item,
)


def print_menu():
    print("\n=== Inventory CLI ===")
    print("1. List all items")
    print("2. Get item by ID")
    print("3. Add a new item")
    print("4. Exit")


def handle_list_items():
    items = get_all_items()
    print("\n--- Inventory Items ---")
    for item in items:
        print(f"ID {item['id']}: {item['name']} (${item['price']}) — stock: {item['stock']}")
    print("-------------------------")


def handle_get_item():
    try:
        item_id = int(input("Enter item ID: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    item = get_item_by_id(item_id)
    if not item:
        print("Item not found.")
    else:
        print("\n--- Item Details ---")
        for key, value in item.items():
            print(f"{key}: {value}")
        print("---------------------")


def handle_add_item():
    print("\nEnter item details:")
    name = input("Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))

    new_item = add_item({"name": name, "price": price, "stock": stock})
    print(f"\nAdded new item with ID {new_item['id']}!")


def run_cli():
    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            handle_list_items()
        elif choice == "2":
            handle_get_item()
        elif choice == "3":
            handle_add_item()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    run_cli()
