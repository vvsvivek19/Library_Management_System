import time
from login_registration import User
import os
from colorama import Fore, Style

def clear_screen():
    """Clears the console screen based on OS."""
    os.system("cls" if os.name == "nt" else "clear")

while True:
    clear_screen()
    try:
        time.sleep(0.1)
        print(Fore.CYAN + "****************************************************" + Style.RESET_ALL)
        print(Fore.LIGHTRED_EX + "           WELCOME TO CENTRAL LIBRARY" + Style.RESET_ALL)
        print(Fore.CYAN + "****************************************************" + Style.RESET_ALL)
        print(Fore.CYAN + "="*53 + Style.RESET_ALL)
        print(Fore.GREEN + "                     HOME MENU                       " + Style.RESET_ALL)
        print(Fore.CYAN + "="*53 + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + "Please choose from below" + Style.RESET_ALL)
        time.sleep(0.1)
        print(Fore.LIGHTCYAN_EX + "1. Login" + Style.RESET_ALL)
        time.sleep(0.1)
        print(Fore.LIGHTCYAN_EX + "2. Register" + Style.RESET_ALL)
        time.sleep(0.1)
        print(Fore.LIGHTCYAN_EX + "3. Exit" + Style.RESET_ALL)
        try:
            choice = int(input(Fore.LIGHTYELLOW_EX + "Please Enter the choice from 1 to 3: " + Style.RESET_ALL)) 
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter a number between 1 and 3." + Style.RESET_ALL)
            input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Wait for user input
            continue

        if choice == 1:
            User.login()
        elif choice == 2:
            User.register()
        elif choice == 3:
            print(Fore.LIGHTGREEN_EX + "\n📖 Knowledge is power...." + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX + "👋 Please visit our library again!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "❌ Invalid input! Please enter a number between 1 and 3." + Style.RESET_ALL)
            input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Wait for user input
            continue
    except Exception as e:
        print(Fore.RED + f"⚠️ An unexpected error occurred: {e}" + Style.RESET_ALL)
        input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Wait for user input

