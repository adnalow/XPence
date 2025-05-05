from ui import Ui
from colorama import Fore

# Product Class
class Product:
    def __init__(self, db, user_id, name="", price=0.0):
        self.db = db
        self.user_id = user_id
        self.name = name
        self.price = price
        self.id = None

    def add_product(self):
        Ui.display_header("Add Product")
        self.name = input(Fore.BLUE + "Enter product name: ").strip()
        if not self.name:
            Ui.display_error("Product name cannot be empty.")
            return
        try:
            self.price = float(input(Fore.BLUE + "Enter product price: "))
        except ValueError:
            Ui.display_error("Invalid price. Please enter a number.")
            return
        if self.price == 0:
            Ui.display_error("Product price cannot be zero.")
            return
        if self.price < 0:
            Ui.display_error("Product price cannot be negative.")
            return
        self.db.execute_query("INSERT INTO products (user_id, name, price) VALUES (?, ?, ?)", (self.user_id, self.name, self.price))
        Ui.display_success("Product added successfully!")

    def remove_product(self):
        products = self.view_products()
        if not products:
            return

        try:
            choice = int(input(Fore.BLUE + "Select a product to remove (number): ")) - 1
            if 0 <= choice < len(products):
                product_id = products[choice][0]
                self.db.execute_query("DELETE FROM products WHERE id = ?", (product_id,))
                self.db.execute_query("DELETE FROM expenses WHERE product_id = ?", (product_id,))
                Ui.display_success("Product removed successfully!")
            else:
                Ui.display_error("Invalid choice.")
        except ValueError:
            Ui.display_error("Invalid input.")

    def view_products(self):
        products = self.db.fetch_all("SELECT id, name, price FROM products WHERE user_id = ?", (self.user_id,))
        
        if not products:
            Ui.display_error("No products found.")
            return []

        Ui.display_header("Products")
        for index, (prod_id, name, price) in enumerate(products, start=1):
            print(Fore.CYAN + f"{index}. {name} - ${price:.2f}")
        print(Fore.YELLOW + "-" * 60)

        return products