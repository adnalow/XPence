import os
import sqlite3

# Function to clear the terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Database setup
conn = sqlite3.connect("business_tracker.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
""")

conn.commit()


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
