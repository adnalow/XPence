import os
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class Ui:
    # Method to clear the terminal screen
    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    # Method to display a header with a title
    @staticmethod
    def display_header(title):
        Ui.clear_screen()
        print(Fore.YELLOW + "=" * 60)
        print(Fore.YELLOW + f"=== {title.upper()} ===")
        print(Fore.YELLOW + "=" * 60)

    # Method to display a box with a message
    @staticmethod
    def display_box(message, color=Fore.GREEN):
        print(color + "+" + "-" * (len(message) + 2) + "+")
        print(color + f"| {message} |")
        print(color + "+" + "-" * (len(message) + 2) + "+")

    # Method to display a list of options in a box
    @staticmethod
    def display_options(options):
        print(Fore.CYAN + "+" + "-" * 30 + "+")
        for index, option in enumerate(options, start=1):
            print(Fore.CYAN + f"| {index}. {option.ljust(26)} |")
        print(Fore.CYAN + "+" + "-" * 30 + "+")

    # Method to display a success message
    @staticmethod
    def display_success(message):
        print(Fore.GREEN + f"✓ {message}")

    # Method to display an error message
    @staticmethod
    def display_error(message):
        print(Fore.RED + f"✗ {message}")
