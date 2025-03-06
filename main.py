import os
import sqlite3


# Function to clear the terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Database setup
conn = sqlite3.connect("business_tracker.db")
cursor = conn.cursor()

# Create tables
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
"""
)

conn.commit()


# User registration
def register():
    clear_screen()
    print("=== Register ===")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        conn.commit()
        print("Registration successful! You can now log in.")
    except sqlite3.IntegrityError:
        print("Username already exists. Try a different one.")


# User login
def login():
    clear_screen()
    print("=== Login ===")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?", (username, password)
    )
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return user[0]
    else:
        print("Invalid credentials. Try again.")
        input("Press Enter to continue...")
        return None


# View products
def view_products(user_id):
    cursor.execute("SELECT id, name, price FROM products WHERE user_id = ?", (user_id,))
    products = cursor.fetchall()

    if not products:
        print("No products found.")
        return []

    print("\n=== Products ===")
    for index, (prod_id, name, price) in enumerate(products, start=1):
        print(f"{index}. {name} - ${price:.2f}")

    return products

# Add a new product
def add_product(user_id):
    print("=== Add Product ===")
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    
    cursor.execute("INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)", (user_id, name, price))
    conn.commit()
    print("Product added successfully!")

# Remove a product
def remove_product(user_id):
    products = view_products(user_id)
    if not products:
        return
    
    try:
        choice = int(input("Select a product to remove (number): ")) - 1
        if 0 <= choice < len(products):
            product_id = products[choice][0]
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            cursor.execute("DELETE FROM expenses WHERE product_id = ?", (product_id,))
            conn.commit()
            print("Product removed successfully!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

# Add an expense
def add_expense(product_id):
    print("=== Add Expense ===")
    name = input("Enter expense name: ")
    amount = float(input("Enter expense amount: "))

    cursor.execute("INSERT INTO expenses (product_id, name, amount) VALUES (?, ?, ?)", (product_id, name, amount))
    conn.commit()
    print("Expense added successfully!")

# Remove an expense
def remove_expense(product_id):
    cursor.execute("SELECT id, name, amount FROM expenses WHERE product_id = ?", (product_id,))
    expenses = cursor.fetchall()
    
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
... (40 lines left)


# Main menu
def main_menu(user_id):
    while True:
        clear_screen()
        print("=== Main Menu ===")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Choose a Product")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            clear_screen()
            view_products(user_id)
            input("Press Enter to continue...")
        elif choice == "2":
            clear_screen()
            add_product(user_id)
            input("Press Enter to continue...")
        elif choice == "3":
            clear_screen()
            remove_product(user_id)
            input("Press Enter to continue...")
        elif choice == "4":
            products = view_products(user_id)
            if not products:
                input("Press Enter to continue...")
                continue
            try:
                prod_choice = int(input("Select a product (number): ")) - 1
                if 0 <= prod_choice < len(products):
                    product_id, product_name, product_price = products[prod_choice]
                    while True:
                        clear_screen()
                        print(f"=== Managing {product_name} ===")
                        print("1. Add Expense")
                        print("2. Remove Expense")
                        print("3. View Product Report")
                        print("4. Simulate Profit")
                        print("5. Go Back")
                        sub_choice = input("Enter your choice: ")

                        if sub_choice == "1":
                            clear_screen()
                            add_expense(product_id)
                        elif sub_choice == "2":
                            clear_screen()
                            remove_expense(product_id)
                        elif sub_choice == "3":
                            clear_screen()
                            view_product_report(product_id, product_price)
                        elif sub_choice == "4":
                            clear_screen()
                            simulate_profit(product_id, product_price)
                        elif sub_choice == "5":
                            break
            except ValueError:
                print("Invalid input.")
        elif choice == "5":
            print("Logging out...\n")
            break


# Program entry point
while True:
    clear_screen()
    print("=== Small Business Expense Tracker ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    user_choice = input("Enter your choice: ")

    if user_choice == "1":
        register()
    elif user_choice == "2":
        user_id = login()
        if user_id:
            main_menu(user_id)
    elif user_choice == "3":
        print("Goodbye!")
        break
