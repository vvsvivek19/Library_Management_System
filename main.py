import time
from users import User

while True:
    try:
        time.sleep(0.1)
        print("****************************************************")
        print("           Welcome to Central Library")
        print("*****************************************************")
        print("Please choose from below")
        time.sleep(0.1)
        print("1. Login")
        time.sleep(0.1)
        print("2. Register")
        time.sleep(0.1)
        print("3. Exit")
        try:
            choice = int(input("Please Enter the choice from 1 to 3: ")) 
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 3.")
            continue

        if choice == 1:
            User.login()
        elif choice == 2:
            User.register()
        elif choice == 3:
            print("\n📖 Knowledge is power....")
            print("👋 Please visit our library again!")
            break
        else:
            print("❌ Invalid input! Please enter a number between 1 and 3.")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")