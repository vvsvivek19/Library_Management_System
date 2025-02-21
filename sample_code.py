import pymysql
import time
import bcrypt
import getpass
from rich.console import Console
from rich.table import Table

# console = Console()

# table = Table(title="Books Available")
# table.add_column("ID", style="cyan")
# table.add_column("Title", style="magenta")
# table.add_column("Author", style="green")

# table.add_row("1", "Python Basics", "John Doe")
# table.add_row("2", "Advanced SQL", "Jane Smith")

# console.print(table)

from colorama import Fore, Style

def test_colors():
    colors = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "BLUE": Fore.BLUE,
        "MAGENTA": Fore.MAGENTA,
        "CYAN": Fore.CYAN,
        "LIGHT RED": Fore.LIGHTRED_EX,
        "LIGHT GREEN": Fore.LIGHTGREEN_EX,
        "LIGHT YELLOW": Fore.LIGHTYELLOW_EX,
        "LIGHT BLUE": Fore.LIGHTBLUE_EX,
        "LIGHT MAGENTA": Fore.LIGHTMAGENTA_EX,
        "LIGHT CYAN": Fore.LIGHTCYAN_EX,
        "WHITE": Fore.WHITE
    }

    print("Testing different colors for user input prompts:\n")
    for name, color in colors.items():
        user_input = input(color + f"Enter your username ({name}): " + Style.RESET_ALL)
        print(Style.RESET_ALL)  # Reset color after input

test_colors()

