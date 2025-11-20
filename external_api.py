# external_api.py

import requests

OPENFOODFACTS_BASE_URL = "https://world.openfoodfacts.org/api/v0/product"


def fetch_product_by_barcode(barcode: str):
    """
    Look up a product in the OpenFoodFacts API by barcode.

    Returns a simplified dict with the fields we care about:
        {
            "barcode": "...",
            "name": "...",
            "brand": "...",
            "ingredients": "..."
        }

    If the product is not found or there is an error, returns None.
    """
    url = f"{OPENFOODFACTS_BASE_URL}/{barcode}.json"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        # For now, just print and return None. In a real app you might use logging.
        print(f"Error calling OpenFoodFacts API: {exc}")
        return None

    data = response.json()

    # OpenFoodFacts uses status = 1 for "product found"
    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "barcode": barcode,
        "name": product.get("product_name") or "Unknown product",
        "brand": product.get("brands"),
        "ingredients": product.get("ingredients_text"),
    }
