import os
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class Ui:
    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def display_header(title):
        Ui.clear_screen()
        print(Fore.CYAN + "╒" + "═" * 58 + "╕")
        print(Fore.CYAN + "│" + Fore.YELLOW + f" {title.upper()} ".center(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "╘" + "═" * 58 + "╛\n")

    @staticmethod
    def display_options(options):
        print(Fore.BLUE + "┌──────────────────────────────────────────────┐")
        for index, option in enumerate(options, start=1):
            opt_text = f" {index}. {option} "
            print(Fore.BLUE + "│" + Fore.CYAN + opt_text.ljust(46) + Fore.BLUE + "│")
        print(Fore.BLUE + "└──────────────────────────────────────────────┘\n")

    @staticmethod
    def styled_input(prompt):
        return input(Fore.BLUE + "➤ " + Fore.MAGENTA + prompt)

    @staticmethod
    def display_success(message):
        print(Fore.GREEN + "✔ " + message)
        print(Fore.GREEN + "─" * 60)

    @staticmethod
    def display_error(message):
        print(Fore.RED + "✖ " + message)
        print(Fore.RED + "─" * 60)

    @staticmethod
    def display_table(headers, data):
        if not data:
            return
            
        # Calculate column widths
        col_widths = [len(header) for header in headers]
        for row in data:
            for i, item in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(item)))
                
        # Create format string
        header_format = "│".join([Fore.BLUE + " %-{}s ".format(w) for w in col_widths])
        row_format = "│".join([Fore.CYAN + " %-{}s ".format(w) for w in col_widths])
        
        # Print table
        print(Fore.BLUE + "┌" + "┬".join(["─" * (w+2) for w in col_widths]) + "┐")
        print(Fore.BLUE + "│" + header_format % tuple(headers) + Fore.BLUE + "│")
        print(Fore.BLUE + "├" + "┼".join(["─" * (w+2) for w in col_widths]) + "┤")
        for row in data:
            print(Fore.BLUE + "│" + row_format % tuple(row) + Fore.BLUE + "│")
        print(Fore.BLUE + "└" + "┴".join(["─" * (w+2) for w in col_widths]) + "┘")

    @staticmethod
    def display_box(message, color=Fore.GREEN):
        box_width = len(message) + 4
        print(color + "╭" + "─" * box_width + "╮")
        print(color + "│  " + message + "  │")
        print(color + "╰" + "─" * box_width + "╯")
