import sqlite3
import unittest
from product import Product
from database import Database
from colorama import Fore, Style


# Create a mock/in-memory db for testing
class TestDatabase(Database):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.create_tables()


def interactive_view_products_test(db, user_id):
    product_manager = Product(db, user_id)
    products = product_manager.view_products()
    input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)


def main():
    db = TestDatabase()

    # Create test users and products
    db.execute_query(
        "INSERT INTO users (username, password) VALUES (?, ?)", ("user1", "pass1")
    )
    db.execute_query(
        "INSERT INTO users (username, password) VALUES (?, ?)", ("user2", "pass2")
    )
    db.execute_query(
        "INSERT INTO users (username, password) VALUES (?, ?)", ("user3", "pass3")
    )

    user1_id = db.fetch_one("SELECT id FROM users WHERE username = ?", ("user1",))[0]
    user2_id = db.fetch_one("SELECT id FROM users WHERE username = ?", ("user2",))[0]
    user3_id = db.fetch_one("SELECT id FROM users WHERE username = ?", ("user3",))[0]
    # Add products for user1
    db.execute_query(
        "INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)",
        (user1_id, "Juice", 12),
    )
    db.execute_query(
        "INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)",
        (user1_id, "Chips", 10),
    )
    db.execute_query(
        "INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)",
        (user1_id, "Lollipop", 1.5),
    )

    # Add products for user2
    db.execute_query(
        "INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)",
        (user2_id, "Cellphone", 200),
    )
    db.execute_query(
        "INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)",
        (user2_id, "Charger", 66),
    )

    while True:
        print("\nView Product Test Case\n")
        print("1. Test User1's Products")
        print("2. Test User2's Products")
        print("3. Test User3's Products/No Products")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            interactive_view_products_test(db, user1_id)
        elif choice == "2":
            interactive_view_products_test(db, user2_id)
        elif choice == "3":
            interactive_view_products_test(db, user3_id)  # No product user
        elif choice == "4":
            print("Exiting test runner.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
