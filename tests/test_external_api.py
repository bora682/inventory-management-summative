from unittest.mock import patch, Mock

from external_api import fetch_product_by_barcode


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_success(mock_get):
    """fetch_product_by_barcode should return a dict when status == 1."""

    # Fake JSON response from OpenFoodFacts
    fake_json = {
        "status": 1,
        "product": {
            "product_name": "Sample Product",
            "brands": "Sample Brand",
            "ingredients_text": "Water, sugar, magic",
        },
    }

    mock_response = Mock()
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_product_by_barcode("1234567890")

    assert isinstance(result, dict)
    assert result["barcode"] == "1234567890"
    assert result["name"] == "Sample Product"
    assert result["brand"] == "Sample Brand"
    assert result["ingredients"] == "Water, sugar, magic"


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_not_found(mock_get):
    """If status != 1, helper should return None."""

    fake_json = {"status": 0}

    mock_response = Mock()
    fake_json = {"status": 0}
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_product_by_barcode("0000000000")
    assert result is None
