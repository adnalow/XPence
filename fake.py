import os
import sqlite3

# Function to clear the terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Function to display a header with a title
def display_header(title):
    clear_screen()
    print("=" * 60)
    print(f"=== {title.upper()} ===")
    print("=" * 60)

# Function to display a box with a message
def display_box(message):
    print("+" + "-" * (len(message) + 2) + "+")
    print(f"| {message} |")
    print("+" + "-" * (len(message) + 2) + "+")

# Function to display a list of options in a box
def display_options(options):
    print("+" + "-" * 30 + "+")
    for index, option in enumerate(options, start=1):
        print(f"| {index}. {option.ljust(26)} |")
    print("+" + "-" * 30 + "+")

# Database Manager
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("business_tracker.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)

        self.conn.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


# User Class
class User:
    def __init__(self, db, username="", password=""):
        self.db = db
        self.username = username
        self.password = password
        self.id = None

    def register(self):
        display_header("Register")
        self.username = input("Enter a username: ")
        self.password = input("Enter a password: ")
        try:
            self.db.execute_query("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password))
            display_box("Registration successful! You can now log in.")
        except sqlite3.IntegrityError:
            display_box("Username already exists. Try a different one.")

    def login(self):
        display_header("Login")
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        user = self.db.fetch_one("SELECT id FROM users WHERE username = ? AND password = ?", (self.username, self.password))
        if user:
            self.id = user[0]
            display_box("Login successful!")
            return True
        else:
            display_box("Invalid credentials. Try again.")
            input("Press Enter to continue...")
            return False


# Product Class
class Product:
    def __init__(self, db, user_id, name="", price=0.0):
        self.db = db
        self.user_id = user_id
        self.name = name
        self.price = price
        self.id = None

    def add_product(self):
        display_header("Add Product")
        self.name = input("Enter product name: ")
        self.price = float(input("Enter product price: "))
        self.db.execute_query("INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)", (self.user_id, self.name, self.price))
        display_box("Product added successfully!")

    def remove_product(self):
        products = self.view_products()
        if not products:
            return

        try:
            choice = int(input("Select a product to remove (number): ")) - 1
            if 0 <= choice < len(products):
                product_id = products[choice][0]
                self.db.execute_query("DELETE FROM products WHERE id = ?", (product_id,))
                self.db.execute_query("DELETE FROM expenses WHERE product_id = ?", (product_id,))
                display_box("Product removed successfully!")
            else:
                display_box("Invalid choice.")
        except ValueError:
            display_box("Invalid input.")

    def view_products(self):
        products = self.db.fetch_all("SELECT id, name, price FROM products WHERE user_id = ?", (self.user_id,))
        
        if not products:
            display_box("No products found.")
            return []

        display_header("Products")
        for index, (prod_id, name, price) in enumerate(products, start=1):
            print(f"{index}. {name} - ${price:.2f}")
        print("-" * 60)

        return products


# Expense Class
class Expense:
    def __init__(self, db, product_id, name="", amount=0.0):
        self.db = db
        self.product_id = product_id
        self.name = name
        self.amount = amount

    def add_expense(self):
        display_header("Add Expense")
        self.name = input("Enter expense name: ")
        self.amount = float(input("Enter expense amount: "))
        self.db.execute_query("INSERT INTO expenses (product_id, name, amount) VALUES (?, ?, ?)", (self.product_id, self.name, self.amount))
        display_box("Expense added successfully!")

    def remove_expense(self):
        expenses = self.db.fetch_all("SELECT id, name, amount FROM expenses WHERE product_id = ?", (self.product_id,))
        
        if not expenses:
            display_box("No expenses found.")
            return

        display_header("Expenses")
        for index, (exp_id, name, amount) in enumerate(expenses, start=1):
            print(f"{index}. {name} - ${amount:.2f}")
        print("-" * 60)

        try:
            choice = int(input("Select an expense to remove (number): ")) - 1
            if 0 <= choice < len(expenses):
                expense_id = expenses[choice][0]
                self.db.execute_query("DELETE FROM expenses WHERE id = ?", (expense_id,))
                display_box("Expense removed successfully!")
        except ValueError:
            display_box("Invalid input.")
            
    def view_product_report(self):
        product = self.db.fetch_one("SELECT price FROM products WHERE id = ?", (self.product_id,))
        if not product:
            display_box("Error: Product not found.")
            return

        price = product[0]
        total_expenses = self.db.fetch_one("SELECT SUM(amount) FROM expenses WHERE product_id = ?", (self.product_id,))[0] or 0

        net_income_per_unit = price - total_expenses
        display_header("Product Report")
        print(f"Product Price: ${price:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net Income Per Unit: ${net_income_per_unit:.2f}")
        print("-" * 60)

    def simulate_profit(self):
        product = self.db.fetch_one("SELECT price FROM products WHERE id = ?", (self.product_id,))
        if not product:
            display_box("Error: Product not found.")
            return

        price = product[0]
        total_expenses = self.db.fetch_one("SELECT SUM(amount) FROM expenses WHERE product_id = ?", (self.product_id,))[0] or 0

        net_income_per_unit = price - total_expenses
        try:
            quantity = int(input("Enter number of products sold: "))
            if quantity < 0:
                display_box("Quantity cannot be negative.")
                return
            total_profit = net_income_per_unit * quantity

            display_header("Profit Simulation")
            print(f"Net Income Per Unit: ${net_income_per_unit:.2f}")
            print(f"Estimated Profit for {quantity} units: ${total_profit:.2f}")
            print("-" * 60)
        except ValueError:
            display_box("Invalid input. Please enter a number.")


# Main Menu
def main_menu(user):
    while True:
        display_header("Main Menu")
        display_options(["View Products", "Add Product", "Remove Product", "Manage Expenses", "Logout"])
        choice = input("Enter your choice: ")

        product_manager = Product(user.db, user.id)

        if choice == "1":
            product_manager.view_products()
            input("Press Enter to continue...")
        elif choice == "2":
            product_manager.add_product()
            input("Press Enter to continue...")
        elif choice == "3":
            product_manager.remove_product()
            input("Press Enter to continue...")
        elif choice == "4":
            products = product_manager.view_products()
            if not products:
                input("Press Enter to continue...")
                continue

            try:
                product_choice = int(input("Select a product to manage expenses (number): ")) - 1
                if 0 <= product_choice < len(products):
                    product_id = products[product_choice][0]
                    manage_expenses(user.db, product_id)
                else:
                    display_box("Invalid choice.")
            except ValueError:
                display_box("Invalid input.")
        elif choice == "5":
            display_box("Logging out...")
            break


# Expense Management Menu
def manage_expenses(db, product_id):
    while True:
        display_header("Expense Management")
        display_options(["View Expenses", "Add Expense", "Remove Expense", "View Product Report", "Simulate Profit", "Go Back"])
        choice = input("Enter your choice: ")

        expense_manager = Expense(db, product_id)

        if choice == "1":
            expenses = db.fetch_all("SELECT name, amount FROM expenses WHERE product_id = ?", (product_id,))
            if not expenses:
                display_box("No expenses found.")
            else:
                display_header("Expenses")
                for index, (name, amount) in enumerate(expenses, start=1):
                    print(f"{index}. {name} - ${amount:.2f}")
                print("-" * 60)
            input("Press Enter to continue...")
        elif choice == "2":
            expense_manager.add_expense()
            input("Press Enter to continue...")
        elif choice == "3":
            expense_manager.remove_expense()
            input("Press Enter to continue...")
        elif choice == "4":
            expense_manager.view_product_report()
            input("Press Enter to continue...")
        elif choice == "5":
            expense_manager.simulate_profit()
            input("Press Enter to continue...")
        elif choice == "6":
            break


# Program Entry Point
def main():
    db = Database()

    while True:
        display_header("Xpense - Small Business Expense Tracker")
        display_options(["Register", "Login", "Exit"])
        user_choice = input("Enter your choice: ")

        user = User(db)

        if user_choice == "1":
            user.register()
        elif user_choice == "2":
            if user.login():
                main_menu(user)
        elif user_choice == "3":
            display_box("Goodbye!")
            break


if __name__ == "__main__":
    main()