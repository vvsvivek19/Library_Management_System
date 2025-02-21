import pymysql
import time
import bcrypt
import getpass

class LibrarySystem:
    
    @classmethod
    def login(cls):
        """Handles login logic for Admin and Student."""
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Vivek1465",
                database="librarydb"
            )
            cursor = conn.cursor()
            
            while True:  # Keep showing menu until a valid choice is made
                cls.clear_screen()
                print("****************************************************")
                print("               Central Library")
                print("*****************************************************")
                print("1. Login as Admin")
                print("2. Login as Student")
                print("3. Go back")

                try:
                    choice = int(input("Are you a student or admin? Please choose from above: "))
                except ValueError:
                    print("❌ Invalid input! Please enter a number (1, 2, or 3).")
                    continue
                
                if choice == 1:
                    cls.admin_login(cursor)
                elif choice == 2:
                    cls.student_login(cursor)
                elif choice == 3:
                    return
                else:
                    print("❌ Invalid Choice! Please select 1, 2, or 3.") 

        except pymysql.MySQLError as err:
            print("❌ Database Error:", err)
        except Exception as general_err:
            print("❌ Unexpected Error:", general_err)
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except Exception as close_err:
                print("❌ Error Closing Connection:", close_err)
    
    @classmethod
    def admin_login(cls, cursor):
        """Handles admin login and menu navigation."""
        print("****************************************************")
        print("-------------------- ADMIN LOGIN --------------------")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        cursor.execute("SELECT password, name FROM admin WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result:
            stored_hashed_password = result[0].encode()  # Convert stored password back to bytes
            if bcrypt.checkpw(password.encode(), stored_hashed_password):
                print(f"\n✅ Welcome {result[1]}! You are logged in as an admin.")
                cls.admin_menu()
            else:
                print("❌ Incorrect password.")
        else:
            print("❌ Admin User not found.")

    @classmethod
    def admin_menu(cls):
        """Displays the admin menu in categorized sections."""
        while True:
            cls.clear_screen()
            print("========== ADMIN MENU ==========")
            print("1. Manage Books")
            print("2. User & Borrowing Management")
            print("3. Reports & Library Policies")
            print("4. Exit to Main Menu")
            
            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue
            
            if choice == 1:
                cls.manage_books()
            elif choice == 2:
                cls.user_borrowing_management()
            elif choice == 3:
                cls.reports_policies()
            elif choice == 4:
                break  # Return to login menu
            else:
                print("❌ Invalid choice! Please select from available options.")

    @classmethod
    def manage_books(cls):
        """Admin menu for book-related actions."""
        while True:
            cls.clear_screen()
            print("========== MANAGE BOOKS ==========")
            print("1. Add a book")
            print("2. Remove a book (Mark unavailable/Permanently delete)")
            print("3. Search a book (by Title/Author/Genre/ISBN)")
            print("4. Display available books")
            print("5. Update book details")
            print("6. Go Back")

            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if choice == 6:
                break  # Return to Admin Menu
            else:
                print(f"⚠️ Feature {choice} not implemented yet!")

    @classmethod
    def user_borrowing_management(cls):
        """Admin menu for managing user interactions and borrowing."""
        while True:
            cls.clear_screen()
            print("========== USER & BORROWING MANAGEMENT ==========")
            print("1. Borrow a book (for admin testing)")
            print("2. Return a book as an admin")
            print("3. View borrow history of a user")
            print("4. View all borrowed books (Check overdue books)")
            print("5. View user details and borrowed books")
            print("6. Go Back")

            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if choice == 6:
                break  # Return to Admin Menu
            else:
                print(f"⚠️ Feature {choice} not implemented yet!")

    @classmethod
    def reports_policies(cls):
        """Admin menu for generating reports and managing policies."""
        while True:
            cls.clear_screen()
            print("========== REPORTS & LIBRARY POLICIES ==========")
            print("1. Fine Calculation")
            print("2. Generate reports (Borrowing trends, Most borrowed books, Overdue fines)")
            print("3. Add/Edit admin users (Super Admin only)")
            print("4. Remove an admin user (Super Admin only)")
            print("5. Update library policies (Fine amount, Borrowing limit)")
            print("6. Send reminders for overdue books (Email/SMS)")
            print("7. Go Back")

            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if choice == 7:
                break  # Return to Admin Menu
            else:
                print(f"⚠️ Feature {choice} not implemented yet!")

    @classmethod
    def student_login(cls, cursor):
        """Placeholder for student login logic (to be implemented later)."""
        print("Student login feature coming soon!")

    @staticmethod
    def clear_screen():
        """Clears the console screen for better readability."""
        print("\n" * 5)
