from ui import Ui
from colorama import Fore

# Expense Class
class Expense:
    def __init__(self, db, product_id, name="", amount=0.0):
        self.db = db
        self.product_id = product_id
        self.name = name
        self.amount = amount

    def add_expense(self):
        Ui.display_header("Add Expense")
        self.name = input(Fore.BLUE + "Enter expense name: ")
        self.amount = float(input(Fore.BLUE + "Enter expense amount: "))
        self.db.execute_query("INSERT INTO expenses (product_id, name, amount) VALUES (?, ?, ?)", (self.product_id, self.name, self.amount))
        Ui.display_success("Expense added successfully!")

    def remove_expense(self):
        expenses = self.db.fetch_all("SELECT id, name, amount FROM expenses WHERE product_id = ?", (self.product_id,))
        
        if not expenses:
            Ui.display_error("No expenses found.")
            return

        Ui.display_header("Expenses")
        for index, (exp_id, name, amount) in enumerate(expenses, start=1):
            print(Fore.CYAN + f"{index}. {name} - ${amount:.2f}")
        print(Fore.YELLOW + "-" * 60)

        try:
            choice = int(input(Fore.BLUE + "Select an expense to remove (number): ")) - 1
            if 0 <= choice < len(expenses):
                expense_id = expenses[choice][0]
                self.db.execute_query("DELETE FROM expenses WHERE id = ?", (expense_id,))
                Ui.display_success("Expense removed successfully!")
        except ValueError:
            Ui.display_error("Invalid input.")
            
    def view_product_report(self):
        product = self.db.fetch_one("SELECT price FROM products WHERE id = ?", (self.product_id,))
        if not product:
            Ui.display_error("Error: Product not found.")
            return

        price = product[0]
        total_expenses = self.db.fetch_one("SELECT SUM(amount) FROM expenses WHERE product_id = ?", (self.product_id,))[0] or 0

        net_income_per_unit = price - total_expenses
        Ui.display_header("Product Report")
        print(Fore.CYAN + f"Product Price: ${price:.2f}")
        print(Fore.CYAN + f"Total Expenses: ${total_expenses:.2f}")
        print(Fore.CYAN + f"Net Income Per Unit: ${net_income_per_unit:.2f}")
        print(Fore.YELLOW + "-" * 60)

    def simulate_profit(self):
        product = self.db.fetch_one("SELECT price FROM products WHERE id = ?", (self.product_id,))
        if not product:
            Ui.display_error("Error: Product not found.")
            return

        price = product[0]
        total_expenses = self.db.fetch_one("SELECT SUM(amount) FROM expenses WHERE product_id = ?", (self.product_id,))[0] or 0

        net_income_per_unit = price - total_expenses
        try:
            quantity = int(input(Fore.BLUE + "Enter number of products sold: "))
            if quantity < 0:
                Ui.display_error("Quantity cannot be negative.")
                return
            total_profit = net_income_per_unit * quantity

            Ui.display_header("Profit Simulation")
            print(Fore.CYAN + f"Net Income Per Unit: ${net_income_per_unit:.2f}")
            print(Fore.CYAN + f"Estimated Profit for {quantity} units: ${total_profit:.2f}")
            print(Fore.YELLOW + "-" * 60)
        except ValueError:
            Ui.display_error("Invalid input. Please enter a number.")
            
    # Expense Management Menu
    def manage_expenses(db, product_id):
        while True:
            Ui.display_header("Expense Management")
            Ui.display_options(["View Expenses", "Add Expense", "Remove Expense", "View Product Report", "Simulate Profit", "Go Back"])
            choice = input(Fore.BLUE + "Enter your choice: ")

            expense_manager = Expense(db, product_id)

            if choice == "1":
                expenses = db.fetch_all("SELECT name, amount FROM expenses WHERE product_id = ?", (product_id,))
                if not expenses:
                    Ui.display_error("No expenses found.")
                else:
                    Ui.display_header("Expenses")
                    for index, (name, amount) in enumerate(expenses, start=1):
                        print(Fore.CYAN + f"{index}. {name} - ${amount:.2f}")
                    print(Fore.YELLOW + "-" * 60)
                input(Fore.YELLOW + "Press Enter to continue...")
            elif choice == "2":
                expense_manager.add_expense()
                input(Fore.YELLOW + "Press Enter to continue...")
            elif choice == "3":
                expense_manager.remove_expense()
                input(Fore.YELLOW + "Press Enter to continue...")
            elif choice == "4":
                expense_manager.view_product_report()
                input(Fore.YELLOW + "Press Enter to continue...")
            elif choice == "5":
                expense_manager.simulate_profit()
                input(Fore.YELLOW + "Press Enter to continue...")
            elif choice == "6":
                break
