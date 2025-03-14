from ui import Ui
import sqlite3
from colorama import Fore

# User Class
class User:
    def __init__(self, db, username="", password=""):
        self.db = db
        self.username = username
        self.password = password
        self.id = None

    def register(self):
        Ui.display_header("Register")
        self.username = input(Fore.BLUE + "Enter a username: ")
        self.password = input(Fore.BLUE + "Enter a password: ")
        try:
            self.db.execute_query("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password))
            Ui.display_success("Registration successful! You can now log in.")
        except sqlite3.IntegrityError:
            Ui.display_error("Username already exists. Try a different one.")

    def login(self):
        Ui.display_header("Login")
        self.username = input(Fore.BLUE + "Enter your username: ")
        self.password = input(Fore.BLUE + "Enter your password: ")
        user = self.db.fetch_one("SELECT id FROM users WHERE username = ? AND password = ?", (self.username, self.password))
        if user:
            self.id = user[0]
            Ui.display_success("Login successful!")
            return True
        else:
            Ui.display_error("Invalid credentials. Try again.")
            input(Fore.YELLOW + "Press Enter to continue...")
            return False