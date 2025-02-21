import time
import pymysql
import bcrypt 
import getpass
from library_management import Library,Book
import os
from colorama import Fore, Style


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
                print(Fore.CYAN + "****************************************************" + Style.RESET_ALL)
                print(Fore.LIGHTRED_EX + "             CENTRAL LIBRARY                   " + Style.RESET_ALL)
                print(Fore.CYAN + "****************************************************" + Style.RESET_ALL)
                print(Fore.CYAN + "="*53 + Style.RESET_ALL)
                print(Fore.GREEN + "                     LOGIN MENU                       " + Style.RESET_ALL)
                print(Fore.CYAN + "="*53 + Style.RESET_ALL)
                time.sleep(0.1)
                print(Fore.LIGHTCYAN_EX + "1. 💼Login as Admin" + Style.RESET_ALL)
                time.sleep(0.1)
                print(Fore.LIGHTCYAN_EX + "2. 🎓Login as Student" + Style.RESET_ALL)
                time.sleep(0.1)
                print(Fore.LIGHTCYAN_EX + "3. 🏡Go back to Home Menu  " + Style.RESET_ALL)
                
                try:
                    choice = int( input(Fore.LIGHTYELLOW_EX +"Are you a student or admin? Please choose: " + Style.RESET_ALL))
                except ValueError:
                    input(Fore.RED + "❌ Invalid input! Please enter a number (1, 2, or 3)." + Style.RESET_ALL)
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
                    input(Fore.LIGHTBLUE_EX  + "Press to continue...." + Style.RESET_ALL)
                    return
                
                #Handling invalid choice
                else:
                    print(Fore.RED + "❌ Invalid Choice! Please select 1, 2, or 3." + Style.RESET_ALL) 
                    input(Fore.LIGHTBLUE_EX  + "Press to continue...." + Style.RESET_ALL)
                    
        except pymysql.MySQLError as err:
             print(Fore.RED + "❌ Error Occurred:", err + Style.RESET_ALL)
        except Exception as general_err:
                print(Fore.RED + "❌ Unexpected Error:", general_err + Style.RESET_ALL)
        finally:
            # Close connection
                try:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
                except Exception as close_err:
                    print(Fore.RED + "❌ Error Closing Connection:", close_err + Style.RESET_ALL)
    
    @classmethod
    def admin_login(cls,cursor):
        cls.clear_screen()
        print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
        print(Fore.GREEN + "--------------------ADMIN LOGIN----------------------" + Style.RESET_ALL)
        print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
        username = input(Fore.LIGHTMAGENTA_EX + "Username: " + Style.RESET_ALL).strip()
        password = getpass.getpass(Fore.LIGHTMAGENTA_EX + "Password: " + Style.RESET_ALL).strip()
        
        #checking if the admin user exists
        cursor.execute("SELECT password, name FROM admin WHERE username = %s ",(username,))
        result = cursor.fetchone()
        if result:
            stored_hashed_password = result[0].encode() # Convert stored password back to bytes
            if bcrypt.checkpw(password.encode(),stored_hashed_password):
                print(Fore.LIGHTGREEN_EX + f"\n✅ Welcome {result[1]}! You are logged in as an admin." + Style.RESET_ALL)
                time.sleep(2)  # Small delay before showing men
                cls.admin_menu()
                return
            else:
                print(Fore.RED + "❌ Incorrect password." + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
        else:
            print(Fore.RED + "❌ Admin User not found." + Style.RESET_ALL)
            input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
    
    @classmethod
    def admin_menu(cls):
        while True:
            cls.clear_screen()
            print(Fore.CYAN + "================================"+ Style.RESET_ALL)
            print(Fore.GREEN + "========== ADMIN MENU ==========" + Style.RESET_ALL)
            print(Fore.CYAN + "================================"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. Book Management" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. User Management" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Borrowing & Returns" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "4. Reports & Policies" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "5. Notifications & Reminders" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "6. Logout" + Style.RESET_ALL)

            try:
                category_choice = int(input(Fore.LIGHTYELLOW_EX + "Enter your choice: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
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
                print(Fore.GREEN + "👋 Logging out..." + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press any key to continue...."+ Style.RESET_ALL)
                break
    
    # Book Management Menu
    @classmethod
    def admin_book_management(cls):
        """Admin menu for book-related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n📚 --Book Management--" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. Add a book" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. Remove a book (Mark as unavailable/Permanently delete)" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Update book details" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "4. Search a book (by Title/Author/Genre/ISBN)" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "5. Display available books" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "6. Go back" + Style.RESET_ALL)

            try:
                book_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue

            if book_choice == 6:
                break  # Go back to main admin menu
            elif book_choice not in [1, 2, 3, 4, 5]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option." + Style.RESET_ALL)
    
    # User Management Menu
    @classmethod
    def admin_user_management(cls):
        """Admin menu for user-related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n👤 --User Management--"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"1. See borrow history of a user"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"2. View user details and borrowed books"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"3. Remove an admin user (Super Admin Only)"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"4. Add/Edit admin users (Super Admin only)"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"5. Go back"+ Style.RESET_ALL)

            try:
                user_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: "+ Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number."+ Style.RESET_ALL)
                continue

            if user_choice == 5:
                break
            elif user_choice not in [1, 2, 3, 4]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option."+ Style.RESET_ALL)
    
    # Borrowing & Returns Menu
    @classmethod
    def admin_borrowing_return_management(cls):
        while True:
            cls.clear_screen()
            print(Fore.GREEN +"\n📖 --Borrowing & Returns--"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"1. Borrow a book (for admin testing)"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"2. Return a book as an admin"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"3. View all borrowed books (Check overdue books)"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"4. Go back"+ Style.RESET_ALL)

            try:
                borrow_choice = int(input(Fore.LIGHTYELLOW_EX +"Choose an option: "+ Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number."+ Style.RESET_ALL)
                continue

            if borrow_choice == 4:
                break
            elif borrow_choice not in [1, 2, 3]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option."+ Style.RESET_ALL)
    
    # Reports & Policies Menu
    @classmethod
    def admin_report_policies_management(cls):
        while True:
            cls.clear_screen()
            print(Fore.GREEN +"\n📊 --Reports & Policies--"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"1. Generate reports (Borrowing trends, Most borrowed books, Overdue fines)"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"2. Fine Calculation"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"3. Update library policies (Fine amount, Borrowing limit)"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"4. Go back"+ Style.RESET_ALL)

            try:
                report_choice = int(input(Fore.LIGHTYELLOW_EX +"Choose an option: "+ Style.RESET_ALL))
            except ValueError:
                input(Fore.RED +"❌ Invalid input! Please enter a valid number."+ Style.RESET_ALL)
                continue

            if report_choice == 4:
                break
            elif report_choice not in [1, 2, 3]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option."+ Style.RESET_ALL)

    # Notifications & Reminders Menu
    @classmethod
    def admin_notification_reminder_management(cls):
        while True:
            cls.clear_screen()
            print(Fore.GREEN +"\n📩 **Notifications & Reminders**"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"1. Send reminders for overdue books (Email/SMS)"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX +"2. Go back"+ Style.RESET_ALL)

            try:
                notify_choice = int(input(Fore.LIGHTYELLOW_EX +"Choose an option: "+ Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number."+ Style.RESET_ALL)
                continue

            if notify_choice == 2:
                break
            elif notify_choice != 1:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option."+ Style.RESET_ALL)
    
    @classmethod
    def student_login(cls, cursor):
        """Placeholder for student login logic (to be implemented later)."""
        while True:
            cls.clear_screen()
            print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
            print(Fore.GREEN + "--------------------STUDENT LOGIN-------------------" + Style.RESET_ALL)
            print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
            try:
                choice = int(input(Fore.LIGHTYELLOW_EX + "Use login method:\n1. Email\n2. Phone Number\nEnter Choice: " + Style.RESET_ALL).strip())
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a number (1 or 2)." + Style.RESET_ALL)
                return
            if choice == 1:
                email = input(Fore.LIGHTMAGENTA_EX + "Email: " + Style.RESET_ALL).strip()
                password = getpass.getpass(Fore.LIGHTMAGENTA_EX + "Password: " + Style.RESET_ALL).strip()
                #checking if the student user exists
                cursor.execute("SELECT password, email FROM users WHERE email = %s ",(email,))
                result = cursor.fetchone()
            elif choice == 2:
                phone = input(Fore.LIGHTMAGENTA_EX + "Phone: " + Style.RESET_ALL).strip()
                password = getpass.getpass(Fore.LIGHTMAGENTA_EX + "Password: " + Style.RESET_ALL)
                #checking if the student user exists
                cursor.execute("SELECT password, phone FROM users WHERE phone = %s ",(phone,))
                result = cursor.fetchone()
            else:
                print(Fore.RED + "❌ Invalid Choice: Please choose either 1 or 2." + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press Enter to try again..." + Style.RESET_ALL)
                continue
            
            if result:
                stored_hashed_password = result[0].encode() # Convert stored password back to bytes
                if bcrypt.checkpw(password.encode(),stored_hashed_password):
                    print(Fore.LIGHTGREEN_EX + f"\n✅ Welcome {result[1]}! You are logged in as an student." + Style.RESET_ALL)
                    time.sleep(2)  # Small delay before showing men
                    cls.student_menu()
                    return
                else:
                    print(Fore.RED + "❌ Incorrect password." + Style.RESET_ALL)
                    input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
            else:
                print(Fore.RED + "❌ Student User not found." + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
                
    @classmethod
    def student_menu(cls):
        print("To be implement.....")
        input("Press any key to exit..")
    
    #REGISTER FUNCTION
    @classmethod
    def register(cls):
        
        while True:
            cls.clear_screen()
            try:
                conn = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="Vivek1465",
                    database="librarydb"
                )
                cursor = conn.cursor()
                time.sleep(0.1)
                print(Fore.CYAN +"****************************************************" + Style.RESET_ALL)
                print(Fore.LIGHTRED_EX + "               Central Library"+ Style.RESET_ALL)
                print(Fore.CYAN +"*****************************************************"+ Style.RESET_ALL)
                print(Fore.CYAN +"="*53+ Style.RESET_ALL)
                print(Fore.GREEN + "                     REGISTER MENU                       "+ Style.RESET_ALL)
                print(Fore.CYAN +"="*53+ Style.RESET_ALL)
                time.sleep(0.1)
                print(Fore.LIGHTYELLOW_EX + "Whom do you want to register as?"+ Style.RESET_ALL)
                time.sleep(0.1)
                print(Fore.LIGHTCYAN_EX + "1. 💼Admin"+ Style.RESET_ALL)
                time.sleep(0.1)
                print(Fore.LIGHTCYAN_EX + "2. 🎓Student"+ Style.RESET_ALL)
                time.sleep(0.1)
                print(Fore.LIGHTCYAN_EX + "3. 🏡Go back to Home Menu"+ Style.RESET_ALL)
                choice = int(input(Fore.LIGHTYELLOW_EX + "Please choose from above options: "+ Style.RESET_ALL))
                
                #Admin Registration Logic
                if choice == 1:
                    time.sleep(0.1)
                    print(Fore.RED + "NOTE: Only admin can register admins!!!"+ Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX + "Please enter the super admin or admin credentials"+ Style.RESET_ALL)
                    username = input(Fore.LIGHTMAGENTA_EX + "Username: "+ Style.RESET_ALL).strip()
                    password = getpass.getpass(Fore.LIGHTMAGENTA_EX + "Password: " + Style.RESET_ALL).strip()
                    cursor.execute("SELECT password, name FROM admin WHERE username = %s ",(username,))
                    result = cursor.fetchone()
                    if result:
                        stored_hashed_password = result[0].encode() # Convert stored password back to bytes
                        if bcrypt.checkpw(password.encode(),stored_hashed_password):
                            cls.clear_screen()
                            print(Fore.CYAN + "="*66 + Style.RESET_ALL)
                            print(Fore.GREEN + "                     ADMIN REGISTRATION                   " + Style.RESET_ALL)
                            print(Fore.CYAN + "="*66 + Style.RESET_ALL)
                            print(Fore.GREEN + f"✅ Welcome {result[1]}! You are authorized to register a new admin."+ Style.RESET_ALL)
                            try:
                                new_admin_username = input(Fore.LIGHTMAGENTA_EX + "Please enter new admin username: "+ Style.RESET_ALL).strip()
                                new_admin_name = input(Fore.LIGHTMAGENTA_EX + "Please enter new admin name: "+ Style.RESET_ALL).strip()
                                new_admin_email = input(Fore.LIGHTMAGENTA_EX + "Please enter new admin email: "+ Style.RESET_ALL).strip()
                                
                                while True:
                                    new_user_phone = input(Fore.LIGHTMAGENTA_EX + "Please enter phone number: "+ Style.RESET_ALL)
                                    if not new_user_phone.isdigit() or len(new_user_phone) < 10:
                                        input(Fore.RED + "❌ Invalid phone number. Please enter a valid 10-digit number."+ Style.RESET_ALL)
                                    else:
                                        break
                                
                                # Check for existing user
                                cursor.execute("SELECT * FROM admin WHERE username = %s OR email = %s OR phone = %s",
                                               (new_admin_username, new_admin_email, new_user_phone))
                                if cursor.fetchone():
                                    input(Fore.RED + "❌ Admin with this username, email, or phone already exists. Try a different one."+ Style.RESET_ALL)
                                    return
                                
                                # Password validation
                                while True:
                                    new_user_password = input(Fore.LIGHTMAGENTA_EX + "Set password: "+ Style.RESET_ALL).strip()
                                    re_enter_password = input(Fore.LIGHTMAGENTA_EX + "Confirm password: "+ Style.RESET_ALL).strip()
                                    if new_user_password == re_enter_password:
                                        break
                                    else:
                                        input("❌ Passwords didn't match! Please try again."+ Style.RESET_ALL)
                                
                                hashed_password = bcrypt.hashpw(new_user_password.encode(), bcrypt.gensalt())
                                cursor.execute("""INSERT INTO admin (username, name, email, phone, password)
                                                VALUES (%s, %s, %s, %s, %s)""",(new_admin_username,new_admin_name,new_admin_email,new_user_phone,hashed_password.decode()))
                                conn.commit()
                                print(Fore.GREEN + "✅ New Admin Registered successfully."+ Style.RESET_ALL)
                                input(Fore.LIGHTRED_EX + "📌 Please remember your username and password!"+ Style.RESET_ALL)
                            
                            except Exception as msg:
                                input(Fore.RED + "Error Occured:"+ Style.RESET_ALL,msg)
                                return
                        else:
                            input(Fore.RED + "❌ Incorrect password."+ Style.RESET_ALL)
                            return
                    else:
                        input(Fore.RED + "❌ Admin User not found."+ Style.RESET_ALL)
                        return
                
                #User Registration Logic 
                elif choice == 2:
                    try:
                        time.sleep(0.1)
                        print(Fore.CYAN + "="*66 + Style.RESET_ALL)
                        print(Fore.GREEN + "                     STUDENT REGISTRATION                " + Style.RESET_ALL)
                        print(Fore.CYAN + "="*66 + Style.RESET_ALL)
                        name = input(Fore.LIGHTMAGENTA_EX + "Enter your name: "+ Style.RESET_ALL).strip()
                        time.sleep(0.1)
                        email = input(Fore.LIGHTMAGENTA_EX + "Enter your email: "+ Style.RESET_ALL).strip()
                        time.sleep(0.1)
                        while True:
                            phone = input(Fore.LIGHTMAGENTA_EX + "Enter your phone number: "+ Style.RESET_ALL).strip()
                            if not phone.isdigit() or len(phone) != 10:
                                input(Fore.RED + "❌ Invalid phone number. Enter a 10-digit number."+ Style.RESET_ALL)
                            else:
                                break #valid phone number
                        
                        # Check for existing user
                        cursor.execute("SELECT * FROM users WHERE email = %s OR phone = %s",
                                            (email, phone))
                        if cursor.fetchone():
                            input(Fore.RED + "❌ User with this email or phone already exists. Try a different one."+ Style.RESET_ALL)
                        
                        # Password validation
                        while True:
                            password = input(Fore.LIGHTMAGENTA_EX + "Set password: "+ Style.RESET_ALL).strip()
                            confirm_password = input(Fore.LIGHTMAGENTA_EX + "Confirm password: "+ Style.RESET_ALL).strip()
                            if password == confirm_password:
                                break
                            input(Fore.RED + "❌ Passwords didn't match! Please try again."+ Style.RESET_ALL)
                        
                        #Hashing the password
                        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                        cursor.execute("""INSERT INTO users (name, email, phone, password)
                                        VALUES (%s, %s, %s, %s)""",(name,email,phone,hashed_password.decode()))
                        conn.commit()
                        print(Fore.GREEN + "✅ User Registered successfully."+ Style.RESET_ALL)
                        input(Fore.LIGHTRED_EX + "📌 Please remember your email and password!"+ Style.RESET_ALL)
                    
                    except Exception as msg:
                        input(Fore.RED + "Error Occured:"+ Style.RESET_ALL,msg)
                
                #Going back Logic
                elif choice == 3:
                    return
                
                #Handling invalid choice
                else:
                    input(Fore.RED + "❌ Invalid Choice! Please select 1, 2, or 3."+ Style.RESET_ALL)        
                        
            except pymysql.MySQLError as err:
                print(Fore.RED + "❌ Error Occurred:"+ Style.RESET_ALL+ Style.RESET_ALL, err)
            except Exception as general_err:
                print(Fore.RED + "❌ Unexpected Error:"+ Style.RESET_ALL, general_err)
            finally:
                # Close connection
                try:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
                except Exception as close_err:
                    print(Fore.RED + "❌ Error Closing Connection:"+ Style.RESET_ALL, close_err)
    
    
    
    #Screen Clearing Method
    @staticmethod
    def clear_screen():
        """Clears the console screen based on OS."""
        os.system("cls" if os.name == "nt" else "clear")
        
    
    
    
    