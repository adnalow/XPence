import builtins
from unittest.mock import patch, MagicMock
from product import Product

def test_add_product():
    db_mock = MagicMock()
    ui_patch = patch("product.Ui")
    input_patch = patch("builtins.input", side_effect=["Notebook", "50.0"])
    
    with ui_patch, input_patch:
        prod = Product(db_mock, user_id=1)
        prod.add_product()
        
        db_mock.execute_query.assert_called_with(
            "INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)",
            (1, "Notebook", 50.0)
        )
        print("Test Add Product: Passed")

if __name__ == "__main__":
    test_add_product()
