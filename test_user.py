import sqlite3
import os
from user import User
from database import Database
from ui import Ui


# create a mock/in memory db for testing
class TestDatabase(Database):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.create_tables()


def interactive_login_test(user):
    print("\n" + "=" * 20)
    print("Login Test Case")
    print("=" * 20)
    result = user.login()


def interactive_register_test(user, valid_credentials):
    print("\n" + "=" * 20)
    print("Register Test Case")
    print("=" * 20)
    user.username = user.username
    user.password = user.password

    try:
        user.register()
        actual = "success"
    except:
        actual = "fail"


def main():
    db = TestDatabase()
    user = User(db)

    # Preload known users
    valid_credentials = {
        "user": "password",
        "monsi": "monsipassword",
        "luna": "lunapassword",
        "angel": "angelpassword",
    }

    for username, password in valid_credentials.items():
        db.execute_query(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )

    while True:
        print("\nLogin/Register Test Case\n")
        print("1. Login Test")
        print("2. Register Test")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            interactive_login_test(user)
        elif choice == "2":
            interactive_register_test(user, valid_credentials)
        elif choice == "3":
            print("Exiting test runner.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
