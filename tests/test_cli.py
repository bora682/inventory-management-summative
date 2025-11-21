from unittest.mock import patch, MagicMock

import cli
import inventory_data


def test_handle_list_items_prints_something():
    """handle_list_items should call get_all_items and print lines."""
    fake_items = [
        {"id": 1, "name": "Item One", "price": 1.0, "stock": 2},
        {"id": 2, "name": "Item Two", "price": 2.0, "stock": 3},
    ]

    with patch.object(inventory_data, "get_all_items", return_value=fake_items):
        with patch("builtins.print") as mock_print:
            cli.handle_list_items()
            # At least one print call should happen
            assert mock_print.call_count > 0


def test_handle_get_item_not_found():
    """If an item is not found, handle_get_item should print a message."""
    with patch.object(inventory_data, "get_item_by_id", return_value=None):
        with patch("builtins.input", return_value="999"):
            with patch("builtins.print") as mock_print:
                cli.handle_get_item()

                # Last print should contain 'Item not found'
                all_calls = [str(call) for call in mock_print.call_args_list]
                assert any("Item not found" in call for call in all_calls)


def test_handle_add_item_creates_item():
    """handle_add_item should call add_item with data built from input."""
    with patch("builtins.input", side_effect=["New Item", "3.5", "10"]):
        with patch.object(cli, "add_item") as mock_add_item:
            mock_add_item.return_value = {
                "id": 99,
                "name": "New Item",
                "price": 3.5,
                "stock": 10,
            }

            with patch("builtins.print") as mock_print:
                cli.handle_add_item()

                mock_add_item.assert_called_once()
                # Confirm something about the print call mentioning ID 99
                all_calls = [str(call) for call in mock_print.call_args_list]
                assert any("99" in call for call in all_calls)
