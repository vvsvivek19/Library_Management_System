import time
import pymysql
import bcrypt 
import getpass
from library_management import Library,Book
import os

class User:

    #LOGIN METHOD
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
            while True: # Keep showing menu until a valid choice is made
                cls.clear_screen()
                time.sleep(0.1)
                print("****************************************************")
                print("               Central Library")
                print("*****************************************************")
                print("="*53)
                print("                     LOGIN MENU                       ")
                print("="*53)
                time.sleep(0.1)
                print("1. Login as Admin")
                time.sleep(0.1)
                print("2. Login as Student")
                time.sleep(0.1)
                print("3. Go back to Home Menu  ")
                
                try:
                    choice = int(input("Are you a student or admin? Please choose from above: "))
                except ValueError:
                    print("❌ Invalid input! Please enter a number (1, 2, or 3).")
                    return
            
                #Loging in as a Admin logic
                if choice == 1:
                    cls.admin_login(cursor)
                
                #Loging in as a student logic
                elif choice == 2:
                    cls.student_login(cursor)
                
                #Going back logic
                elif choice == 3:
                    print("Going back to home page.....")
                    return
                
                #Handling invalid choice
                else:
                    print("❌ Invalid Choice! Please select 1, 2, or 3.") 
                    
        except pymysql.MySQLError as err:
             print("❌ Error Occurred:", err)
        except Exception as general_err:
                print("❌ Unexpected Error:", general_err)
        finally:
            # Close connection
                try:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
                except Exception as close_err:
                    print("❌ Error Closing Connection:", close_err)
    
    @classmethod
    def admin_login(cls,cursor):
        print("****************************************************")
        print("--------------------ADMIN LOGIN----------------------")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        
        #checking if the admin user exists
        cursor.execute("SELECT password, name FROM admin WHERE username = %s ",(username,))
        result = cursor.fetchone()
        if result:
            stored_hashed_password = result[0].encode() # Convert stored password back to bytes
            if bcrypt.checkpw(password.encode(),stored_hashed_password):
                print(f"\n✅ Welcome {result[1]}! You are logged in as an admin.")
                # time.sleep(1)  # Small delay before showing men
                cls.admin_menu()
                return
            else:
                print("❌ Incorrect password.")
                input("Press Enter to continue...")  # Pause before returning to login
        else:
            print("❌ Admin User not found.")
            input("Press Enter to continue...")  # Pause before returning to login
    
    @classmethod
    def admin_menu(cls):
        while True:
            cls.clear_screen()
            print("========== ADMIN MENU ==========")
            print("1. Book Management")
            print("2. User Management")
            print("3. Borrowing & Returns")
            print("4. Reports & Policies")
            print("5. Notifications & Reminders")
            print("6. Logout")

            try:
                category_choice = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue
            
            if category_choice == 1:
                cls.admin_book_management()
            elif category_choice == 2:
                cls.admin_user_management()
            elif category_choice == 3:
                cls.admin_borrowing_return_management()
            elif category_choice == 4:
                cls.admin_report_policies_management()
            elif category_choice == 5:
                cls.admin_notification_reminder_management()
            elif category_choice == 6:
                print("👋 Logging out...")
                break
    
    # Book Management Menu
    @classmethod
    def admin_book_management(cls):
        """Admin menu for book-related actions."""
        while True:
            cls.clear_screen()
            print("\n📚 **Book Management**")
            print("1. Add a book")
            print("2. Remove a book (Mark as unavailable/Permanently delete)")
            print("3. Update book details")
            print("4. Search a book (by Title/Author/Genre/ISBN)")
            print("5. Display available books")
            print("6. Go back")

            try:
                book_choice = int(input("Choose an option: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if book_choice == 6:
                break  # Go back to main admin menu
            elif book_choice not in [1, 2, 3, 4, 5]:
                print("❌ Invalid option! Please choose a valid option.")
    
    # User Management Menu
    @classmethod
    def admin_user_management(cls):
        """Admin menu for user-related actions."""
        while True:
            cls.clear_screen()
            print("\n👤 **User Management**")
            print("1. See borrow history of a user")
            print("2. View user details and borrowed books")
            print("3. Remove an admin user (Super Admin Only)")
            print("4. Add/Edit admin users (Super Admin only)")
            print("5. Go back")

            try:
                user_choice = int(input("Choose an option: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if user_choice == 5:
                break
            elif user_choice not in [1, 2, 3, 4]:
                print("❌ Invalid option! Please choose a valid option.")
    
    # Borrowing & Returns Menu
    @classmethod
    def admin_borrowing_return_management(cls):
        while True:
            cls.clear_screen()
            print("\n📖 **Borrowing & Returns**")
            print("1. Borrow a book (for admin testing)")
            print("2. Return a book as an admin")
            print("3. View all borrowed books (Check overdue books)")
            print("4. Go back")

            try:
                borrow_choice = int(input("Choose an option: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if borrow_choice == 4:
                break
            elif borrow_choice not in [1, 2, 3]:
                print("❌ Invalid option! Please choose a valid option.")
    
    # Reports & Policies Menu
    @classmethod
    def admin_report_policies_management(cls):
        while True:
            cls.clear_screen()
            print("\n📊 **Reports & Policies**")
            print("1. Generate reports (Borrowing trends, Most borrowed books, Overdue fines)")
            print("2. Fine Calculation")
            print("3. Update library policies (Fine amount, Borrowing limit)")
            print("4. Go back")

            try:
                report_choice = int(input("Choose an option: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if report_choice == 4:
                break
            elif report_choice not in [1, 2, 3]:
                print("❌ Invalid option! Please choose a valid option.")

    # Notifications & Reminders Menu
    @classmethod
    def admin_notification_reminder_management(cls):
        while True:
            print("\n📩 **Notifications & Reminders**")
            print("1. Send reminders for overdue books (Email/SMS)")
            print("2. Go back")

            try:
                notify_choice = int(input("Choose an option: "))
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                continue

            if notify_choice == 2:
                break
            elif notify_choice != 1:
                print("❌ Invalid option! Please choose a valid option.")
    
    @classmethod
    def student_login(cls, cursor):
        """Placeholder for student login logic (to be implemented later)."""
        print("Student login feature coming soon!")
        
    #REGISTER FUNCTION
    @classmethod
    def register(cls):
        cls.clear_screen()
        while True:
            try:
                conn = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="Vivek1465",
                    database="librarydb"
                )
                cursor = conn.cursor()
                time.sleep(0.1)
                print("****************************************************")
                print("               Central Library")
                print("*****************************************************")
                print("="*53)
                print("                     REGISTER MENU                       ")
                print("="*53)
                time.sleep(0.1)
                print("Whom do you want to register as?")
                time.sleep(0.1)
                print("1. Admin")
                time.sleep(0.1)
                print("2. Student")
                time.sleep(0.1)
                print("3. Go back")
                choice = int(input("Please choose from above options: "))
                
                #Admin Registration Logic
                if choice == 1:
                    time.sleep(0.1)
                    print("****************************************************")
                    print("Only admin can register admins!!!")
                    print("Please enter the super admin or admin credentials")
                    username = input("Username: ").strip()
                    password = input("password: ").strip()
                    cursor.execute("SELECT password, name FROM admin WHERE username = %s ",(username,))
                    result = cursor.fetchone()
                    if result:
                        stored_hashed_password = result[0].encode() # Convert stored password back to bytes
                        if bcrypt.checkpw(password.encode(),stored_hashed_password):
                            print(f"✅ Welcome {result[1]}! You are authorized to register a new admin.")
                            try:
                                new_admin_username = input("Please enter new admin username: ").strip()
                                new_admin_name = input("Please enter new admin name: ").strip()
                                new_admin_email = input("Please enter new admin email: ").strip()
                                
                                while True:
                                    new_user_phone = input("Please enter phone number: ")
                                    if not new_user_phone.isdigit() or len(new_user_phone) < 10:
                                        print("❌ Invalid phone number. Please enter a valid 10-digit number.")
                                    else:
                                        break
                                
                                # Check for existing user
                                cursor.execute("SELECT * FROM admin WHERE username = %s OR email = %s OR phone = %s",
                                               (new_admin_username, new_admin_email, new_user_phone))
                                if cursor.fetchone():
                                    print("❌ Admin with this username, email, or phone already exists. Try a different one.")
                                    return
                                
                                # Password validation
                                while True:
                                    new_user_password = input("Set password: ").strip()
                                    re_enter_password = input("Confirm password: ").strip()
                                    if new_user_password == re_enter_password:
                                        break
                                    else:
                                        print("❌ Passwords didn't match! Please try again.")
                                
                                hashed_password = bcrypt.hashpw(new_user_password.encode(), bcrypt.gensalt())
                                cursor.execute("""INSERT INTO admin (username, name, email, phone, password)
                                                VALUES (%s, %s, %s, %s, %s)""",(new_admin_username,new_admin_name,new_admin_email,new_user_phone,hashed_password.decode()))
                                conn.commit()
                                print("✅ New Admin Registered successfully.")
                                print("📌 Please remember your username and password!")
                            
                            except Exception as msg:
                                print("Error Occured:",msg)
                                return
                        else:
                            print("❌ Incorrect password.")
                            return
                    else:
                        print("❌ Admin User not found.")
                        return
                
                #User Registration Logic 
                elif choice == 2:
                    try:
                        time.sleep(0.1)
                        print("****************************************************")
                        name = input("Enter your name: ").strip()
                        time.sleep(0.1)
                        email = input("Enter your email: ").strip()
                        time.sleep(0.1)
                        while True:
                            phone = input("Enter your phone number: ").strip()
                            if not phone.isdigit() or len(phone) != 10:
                                print("❌ Invalid phone number. Enter a 10-digit number.")
                            else:
                                break #valid phone number
                        
                        # Check for existing user
                        cursor.execute("SELECT * FROM users WHERE email = %s OR phone = %s",
                                            (email, phone))
                        if cursor.fetchone():
                            print("❌ User with this email or phone already exists. Try a different one.")
                        
                        # Password validation
                        while True:
                            password = input("Set password: ").strip()
                            confirm_password = input("Confirm password: ").strip()
                            if password == confirm_password:
                                break
                            print("❌ Passwords didn't match! Please try again.")
                        
                        #Hashing the password
                        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                        cursor.execute("""INSERT INTO users (name, email, phone, password)
                                        VALUES (%s, %s, %s, %s)""",(name,email,phone,hashed_password.decode()))
                        conn.commit()
                        print("✅ User Registered successfully.")
                        print("📌 Please remember your username and password!")
                    
                    except Exception as msg:
                        print("Error Occured:",msg)
                
                #Going back Logic
                elif choice == 3:
                    return
                
                #Handling invalid choice
                else:
                    print("❌ Invalid Choice! Please select 1, 2, or 3.")        
                        
            except pymysql.MySQLError as err:
                print("❌ Error Occurred:", err)
            except Exception as general_err:
                print("❌ Unexpected Error:", general_err)
            finally:
                # Close connection
                try:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
                except Exception as close_err:
                    print("❌ Error Closing Connection:", close_err)
    
    
    
    #Screen Clearing Method
    @staticmethod
    def clear_screen():
        """Clears the console screen based on OS."""
        os.system("cls" if os.name == "nt" else "clear")
        
    
    
    
    