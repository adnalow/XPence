from ui import Ui
from user import User
from product import Product
from expense import Expense
from database import Database
from colorama import Fore

# Main Menu
def main_menu(user):
    while True:
        Ui.display_header("Main Menu")
        Ui.display_options(["View Products", "Add Product", "Remove Product", "Manage Expenses", "Logout"])
        choice = input(Fore.BLUE + "Enter your choice: ")

        product_manager = Product(user.db, user.id)

        if choice == "1":
            product_manager.view_products()
            input(Fore.YELLOW + "Press Enter to continue...")
        elif choice == "2":
            product_manager.add_product()
            input(Fore.YELLOW + "Press Enter to continue...")
        elif choice == "3":
            product_manager.remove_product()
            input(Fore.YELLOW + "Press Enter to continue...")
        elif choice == "4":
            products = product_manager.view_products()
            if not products:
                input(Fore.YELLOW + "Press Enter to continue...")
                continue

            try:
                product_choice = int(input(Fore.BLUE + "Select a product to manage expenses (number): ")) - 1
                if 0 <= product_choice < len(products):
                    product_id = products[product_choice][0]
                    Expense.manage_expenses(user.db, product_id)
                else:
                    Ui.display_error("Invalid choice.")
            except ValueError:
                Ui.display_error("Invalid input.")
        elif choice == "5":
            Ui.display_box("Logging out...", Fore.YELLOW)
            break





# Program Entry Point
def main():
    db = Database()

    while True:
        Ui.display_header("Xpense - Small Business Expense Tracker")
        Ui.display_options(["Register", "Login", "Exit"])
        user_choice = input(Fore.BLUE + "Enter your choice: ")

        user = User(db)

        if user_choice == "1":
            user.register()
        elif user_choice == "2":
            if user.login():
                main_menu(user)
        elif user_choice == "3":
            Ui.display_box("Goodbye!", Fore.YELLOW)
            break


if __name__ == "__main__":
    main()