import os
import sqlite3

# Function to clear the terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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
        clear_screen()
        print("=== Register ===")
        self.username = input("Enter a username: ")
        self.password = input("Enter a password: ")
        try:
            self.db.execute_query("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password))
            print("Registration successful! You can now log in.")
        except sqlite3.IntegrityError:
            print("Username already exists. Try a different one.")

    def login(self):
        clear_screen()
        print("=== Login ===")
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        user = self.db.fetch_one("SELECT id FROM users WHERE username = ? AND password = ?", (self.username, self.password))
        if user:
            self.id = user[0]
            print("Login successful!")
            return True
        else:
            print("Invalid credentials. Try again.")
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
        print("=== Add Product ===")
        self.name = input("Enter product name: ")
        self.price = float(input("Enter product price: "))
        self.db.execute_query("INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)", (self.user_id, self.name, self.price))
        print("Product added successfully!")

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
                print("Product removed successfully!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

    def view_products(self):
        products = self.db.fetch_all("SELECT id, name, price FROM products WHERE user_id = ?", (self.user_id,))
        
        if not products:
            print("No products found.")
            return []

        print("\n=== Products ===")
        for index, (prod_id, name, price) in enumerate(products, start=1):
            print(f"{index}. {name} - ${price:.2f}")

        return products


# Expense Class
class Expense:
    def __init__(self, db, product_id, name="", amount=0.0):
        self.db = db
        self.product_id = product_id
        self.name = name
        self.amount = amount

    def add_expense(self):
        print("=== Add Expense ===")
        self.name = input("Enter expense name: ")
        self.amount = float(input("Enter expense amount: "))
        self.db.execute_query("INSERT INTO expenses (product_id, name, amount) VALUES (?, ?, ?)", (self.product_id, self.name, self.amount))
        print("Expense added successfully!")

    def remove_expense(self):
        expenses = self.db.fetch_all("SELECT id, name, amount FROM expenses WHERE product_id = ?", (self.product_id,))
        
        if not expenses:
            print("No expenses found.")
            return

        print("\n=== Expenses ===")
        for index, (exp_id, name, amount) in enumerate(expenses, start=1):
            print(f"{index}. {name} - ${amount:.2f}")

        try:
            choice = int(input("Select an expense to remove (number): ")) - 1
            if 0 <= choice < len(expenses):
                expense_id = expenses[choice][0]
                self.db.execute_query("DELETE FROM expenses WHERE id = ?", (expense_id,))
                print("Expense removed successfully!")
        except ValueError:
            print("Invalid input.")
            
    def view_product_report(self):
        # Fetch product price
        product = self.db.fetch_one("SELECT price FROM products WHERE id = ?", (self.product_id,))
        if not product:
            print("Error: Product not found.")
            return

        price = product[0]  # Extract price from tuple
        total_expenses = self.db.fetch_one("SELECT SUM(amount) FROM expenses WHERE product_id = ?", (self.product_id,))[0] or 0

        net_income_per_unit = price - total_expenses
        print("\n=== Product Report ===")
        print(f"Product Price: ${price:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net Income Per Unit: ${net_income_per_unit:.2f}")

    def simulate_profit(self):
        # Fetch product price
        product = self.db.fetch_one("SELECT price FROM products WHERE id = ?", (self.product_id,))
        if not product:
            print("Error: Product not found.")
            return

        price = product[0]  # Extract price from tuple
        total_expenses = self.db.fetch_one("SELECT SUM(amount) FROM expenses WHERE product_id = ?", (self.product_id,))[0] or 0

        net_income_per_unit = price - total_expenses
        try:
            quantity = int(input("Enter number of products sold: "))
            if quantity < 0:
                print("Quantity cannot be negative.")
                return
            total_profit = net_income_per_unit * quantity  # Total profit calculation

            print("\n=== Profit Simulation ===")
            print(f"Net Income Per Unit: ${net_income_per_unit:.2f}")
            print(f"Estimated Profit for {quantity} units: ${total_profit:.2f}")
        except ValueError:
            print("Invalid input. Please enter a number.")
        


# Main Menu
def main_menu(user):
    while True:
        clear_screen()
        print("=== Main Menu ===")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Choose a Product to Manage Expenses")
        print("5. Logout")
        choice = input("Enter your choice: ")

        product_manager = Product(user.db, user.id)

        if choice == "1":
            clear_screen()
            product_manager.view_products()
            input("Press Enter to continue...")
        elif choice == "2":
            clear_screen()
            product_manager.add_product()
            input("Press Enter to continue...")
        elif choice == "3":
            clear_screen()
            product_manager.remove_product()
            input("Press Enter to continue...")
        elif choice == "4":
            clear_screen()
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
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")

        elif choice == "5":
            print("Logging out...\n")
            break


# Expense Management Menu
def manage_expenses(db, product_id):
    while True:
        clear_screen()
        print("=== Expense Management ===")
        print("1. View Expenses")
        print("2. Add Expense")
        print("3. Remove Expense")
        print("4. View Product Report")
        print("5. Simulate Profit")
        print("6. Go Back")

        expense_manager = Expense(db, product_id)
        choice = input("Enter your choice: ")

        if choice == "1":  # View Expenses (No Deletion)
            clear_screen()
            expenses = db.fetch_all("SELECT name, amount FROM expenses WHERE product_id = ?", (product_id,))
            
            if not expenses:
                print("No expenses found.")
            else:
                print("\n=== Expenses ===")
                for index, (name, amount) in enumerate(expenses, start=1):
                    print(f"{index}. {name} - ${amount:.2f}")

            input("\nPress Enter to continue...")

        elif choice == "2":  # Add Expense
            clear_screen()
            expense_manager.add_expense()
            input("Press Enter to continue...")

        elif choice == "3":  # Remove Expense
            clear_screen()
            expense_manager.remove_expense()
            input("Press Enter to continue...")
            
        elif choice == "4":  # View Product Report
            clear_screen()
            expense_manager.view_product_report()
            input("Press Enter to continue...")

        elif choice == "5":  # Simulate Profit
            clear_screen()
            expense_manager.simulate_profit()
            input("Press Enter to continue...")

        elif choice == "6":  # Go Back
            break



# Program Entry Point
def main():
    db = Database()

    while True:
        clear_screen()
        print("=== Small Business Expense Tracker ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        user_choice = input("Enter your choice: ")

        user = User(db)

        if user_choice == "1":
            user.register()
        elif user_choice == "2":
            if user.login():
                main_menu(user)
        elif user_choice == "3":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
