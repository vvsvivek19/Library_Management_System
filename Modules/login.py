'''
Importing Important modules - both native and external
'''
import time
import pymysql
import bcrypt 
import getpass
import os
from colorama import Fore, Style
from Modules.utils import SECURITY_QUESTIONS


class Login:
#-----------------------------------------------------------------------------------------------------
    #LOGIN METHOD
#-----------------------------------------------------------------------------------------------------
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
            print(Fore.RED + "❌ Error Occurred:" +  str(err) + Style.RESET_ALL)
        except Exception as general_err:
            print(Fore.RED + "❌ Unexpected Error:" + str(general_err) + Style.RESET_ALL)
            import traceback
            traceback.print_exc()
            time.sleep(30)
        finally:
            # Close connection
                try:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
                except Exception as close_err:
                    print(Fore.RED + "❌ Error Closing Connection:", close_err + Style.RESET_ALL)
#-----------------------------------------------------------------------------------------------------
    #ADMIN LOGIN METHOD
#-----------------------------------------------------------------------------------------------------
    @classmethod
    def admin_login(cls,cursor):
        max_password_attempt = 3
        password_attempt = 0
        while password_attempt < max_password_attempt:
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
                    cursor.execute("SELECT ans_1 from admin where username = %s",(username,))
                    stored_answer = cursor.fetchone()[0]
                    if stored_answer is None or bcrypt.checkpw("DefaultAnswer123".encode(),stored_answer.encode()):
                        print(Fore.YELLOW + "\n⚠️ Security Alert: Please update your security questions!" + Style.RESET_ALL)
                        time.sleep(2)
                        cls.admin_update_security_questions(cursor, username)                
                    time.sleep(2)  # Small delay before showing men
                    password_attempt = 0
                    cls.admin_menu()
                    return
                else:
                    password_attempt += 1
                    print(Fore.RED + f"❌ Incorrect password. Attempts left: {max_password_attempt - password_attempt}" + Style.RESET_ALL)
                    input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
            else:
                password_attempt += 1
                print(Fore.RED + f"❌ Admin User not found. Attempts left: {max_password_attempt - password_attempt}" + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
         
        print(Fore.RED + "❌ Too many failed attempts! Please Contact Super User." + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "Going back to Login Menu..." + Style.RESET_ALL)
        time.sleep(2)
        return
    
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
            print(Fore.LIGHTCYAN_EX + "6. Account Management" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "7. Logout" + Style.RESET_ALL)

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
                cls.admin_account_management()
            elif category_choice == 7:
                print(Fore.GREEN + "👋 Logging out..." + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press any key to continue...."+ Style.RESET_ALL)
                break
    
    # Admin Book Management Menu
    @classmethod
    def admin_book_management(cls):
        """Admin menu for book-related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n📚 --Admin Book Management--" + Style.RESET_ALL)
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
    
    #Admin Account Management menu
    @classmethod
    def admin_account_management(cls):
        """admin menu for Account Management related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n👤-- Admin Account Management--" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. Update Profile" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. Update Password" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Update Security Questions" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "4. Go back" + Style.RESET_ALL)

            try:
                book_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue

            if book_choice == 4:
                return  # Go back to main student menu
            elif book_choice not in [1,2,3]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option." + Style.RESET_ALL)
    
#-----------------------------------------------------------------------------------------------------
    #STUDENT LOGIN METHOD
#-----------------------------------------------------------------------------------------------------    
    @classmethod
    def student_login(cls, cursor):
        max_password_attempt = 3 # Max allowed attempts
        password_attempt = 0 # Track failed attempts
        while password_attempt < max_password_attempt:
            cls.clear_screen()
            print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
            print(Fore.GREEN + "--------------------STUDENT LOGIN-------------------" + Style.RESET_ALL)
            print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
            try:
                choice = int(input(Fore.LIGHTYELLOW_EX + "Use login method:\n1. Email\n2. Phone Number\n3. Exit to Login menu\nEnter Choice: " + Style.RESET_ALL).strip())
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a number (1 or 2)." + Style.RESET_ALL)
                return
            
            #checking if the student user exists
            if choice == 1:
                email = input(Fore.LIGHTMAGENTA_EX + "Email: " + Style.RESET_ALL).strip()
                password = getpass.getpass(Fore.LIGHTMAGENTA_EX + "Password: " + Style.RESET_ALL).strip()
                #checking if the student user exists
                cursor.execute("SELECT name, password, email FROM users WHERE email = %s ",(email,))
                result = cursor.fetchone()
            elif choice == 2:
                phone = input(Fore.LIGHTMAGENTA_EX + "Phone: " + Style.RESET_ALL).strip()
                password = getpass.getpass(Fore.LIGHTMAGENTA_EX + "Password: " + Style.RESET_ALL)
                #checking if the student user exists
                cursor.execute("SELECT name, password, phone FROM users WHERE phone = %s ",(phone,))
                result = cursor.fetchone()
            elif choice == 3:
                print(Fore.LIGHTBLUE_EX + "🔙 Going back to Login menu..." + Style.RESET_ALL)
                time.sleep(1)
                return
            else:
                print(Fore.RED + "❌ Invalid Choice: Please choose either 1, 2, or 3." + Style.RESET_ALL)
                try:
                    user_exit_choice = int(input("Press 1 to try again or press 2 to exit to login menu: "))
                    if user_exit_choice == 1:
                        print(Fore.LIGHTBLUE_EX + "🔄 Please enter the credentials again..." + Style.RESET_ALL)
                        continue
                    else:
                        print(Fore.LIGHTBLUE_EX + "🔙 Going back to Login menu..." + Style.RESET_ALL)
                        time.sleep(1)
                        return  # Fully exit the function
                except ValueError:
                    print(Fore.RED + "❌ Invalid input! Returning to login menu..." + Style.RESET_ALL)
                    time.sleep(1)
                    return  # Exit on invalid input
            
            if result:
                stored_hashed_password = result[1].encode() # Convert stored password back to bytes
                if bcrypt.checkpw(password.encode(),stored_hashed_password):
                    print(Fore.LIGHTGREEN_EX + f"\n✅ Welcome {result[0]}... You are logged in as an student." + Style.RESET_ALL)
                    if choice == 1:
                        cursor.execute("SELECT ans_1 from users where email = %s",(email,))
                        stored_answer = cursor.fetchone()[0]
                        if stored_answer is None or bcrypt.checkpw("DefaultAnswer123".encode(),stored_answer.encode()):
                            print(Fore.YELLOW + "\n⚠️ Security Alert: Please update your security questions!" + Style.RESET_ALL)
                            time.sleep(2)
                            cls.student_update_security_questions(cursor, email)
                    elif choice == 2:
                        cursor.execute("SELECT ans_1 from users where phone = %s",(phone,))
                        stored_answer = cursor.fetchone()[0]
                        if  stored_answer is None or bcrypt.checkpw("DefaultAnswer123".encode(),stored_answer.encode()):
                            print(Fore.YELLOW + "\n⚠️ Security Alert: Please update your security questions!" + Style.RESET_ALL)
                            time.sleep(2)
                            cls.student_update_security_questions(cursor, phone)
                    time.sleep(2)  # Small delay before showing menu
                    password_attempt = 0
                    cls.student_menu()
                    return
                else:
                    password_attempt += 1
                    print(Fore.RED + f"❌ Incorrect password. Attempts left: {max_password_attempt - password_attempt}" + Style.RESET_ALL)
                    input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
            else:
                password_attempt += 1
                print(Fore.RED + f"❌ Student User not found. Attempts left: {max_password_attempt - password_attempt}" + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to login
            
        print(Fore.RED + "❌ Too many failed attempts! Try again later." + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "Going back to Login Menu..." + Style.RESET_ALL)
        time.sleep(2)
        return
                
                
    @classmethod
    def student_menu(cls):
         while True:
            cls.clear_screen()
            print(Fore.CYAN + "================================"+ Style.RESET_ALL)
            print(Fore.GREEN + "========== STUDENT MENU =======" + Style.RESET_ALL)
            print(Fore.CYAN + "================================"+ Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. 🔍 Book Management" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. 📖 Borrowing & Returns" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. 💰 Fines & Due Dates" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "4. 👤 Account Management" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "5. ✨ Additional Features (Optional for Later)" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "6. 🔙 Logout" + Style.RESET_ALL)

            try:
                category_choice = int(input(Fore.LIGHTYELLOW_EX + "Enter your choice: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue
            
            if category_choice == 1:
                cls.student_book_management()
            elif category_choice == 2:
                cls.student_borrowing_returns()
            elif category_choice == 3:
                cls.student_fines_due_dates()
            elif category_choice == 4:
                cls.student_account_management()
            elif category_choice == 5:
                cls.student_additional_features()
            elif category_choice == 6:
                print(Fore.GREEN + "👋 Logging out..." + Style.RESET_ALL)
                input(Fore.LIGHTBLUE_EX + "Press any key to continue...."+ Style.RESET_ALL)
                break
    
    #Student Book Management Menu
    @classmethod
    def student_book_management(cls):
        """student menu for book-related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n📚 --Student Book Management--" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. Display available books" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. Search a book (by Title/Author/Genre/ISBN)" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Go back" + Style.RESET_ALL)

            try:
                book_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue

            if book_choice == 3:
                return  # Go back to main student menu
            elif book_choice not in [1, 2]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option." + Style.RESET_ALL)
    
    #Student Borrowing & Returns menu
    @classmethod
    def student_borrowing_returns(cls):
        """student menu for Borrowing & Returns related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n📖-- Student Borrowing & Returns--" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. Borrow a Book" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. Return a Book" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Renew a Book" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "4. Go back" + Style.RESET_ALL)

            try:
                book_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue

            if book_choice == 4:
                return  # Go back to main student menu
            elif book_choice not in [1, 2, 3]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option." + Style.RESET_ALL)
    
    #Student Fines & Due Dates menu
    @classmethod
    def student_fines_due_dates(cls):
        """student menu for Fines & Due Date related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n💰-- Student Fines & Due Dates--" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. View Borrowed Books" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. Check Fine" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Go back" + Style.RESET_ALL)

            try:
                book_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue

            if book_choice == 3:
                return  # Go back to main student menu
            elif book_choice not in [1, 2]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option." + Style.RESET_ALL)
    
    #Student Account Management menu
    @classmethod
    def student_account_management(cls):
        """student menu for Account Management related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n👤-- Student Account Management--" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. Update Profile" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. Update Password" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Update Security Questions" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "4. Go back" + Style.RESET_ALL)

            try:
                book_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue

            if book_choice == 4:
                return  # Go back to main student menu
            elif book_choice not in [1,2,3]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option." + Style.RESET_ALL)
    
    #Student  Additional Features (Optional for Later) menu
    @classmethod
    def student_additional_features(cls):
        """student menu for  Additional Features (Optional for Later) related actions."""
        while True:
            cls.clear_screen()
            print(Fore.GREEN + "\n✨-- Student  Additional Features (Optional for Later)--" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1. Request a Book" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "2. Reserve a Book" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "3. Feedback/Complaints" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "4. Go Back" + Style.RESET_ALL)

            try:
                book_choice = int(input(Fore.LIGHTYELLOW_EX + "Choose an option: " + Style.RESET_ALL))
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                continue

            if book_choice == 4:
                return  # Go back to main student menu
            elif book_choice not in [1, 2,3]:
                input(Fore.RED + "❌ Invalid option! Please choose a valid option." + Style.RESET_ALL)
    
#-----------------------------------------------------------------------------------------------------
# STATIC METHOD TO UPDATE SECURITY QUESTIONS FOR EXISTING ADMIN USER
#-----------------------------------------------------------------------------------------------------
    @staticmethod
    def admin_update_security_questions(cursor, username):
        
        print(Fore.LIGHTYELLOW_EX + "Select 3 questions from below list of questions: " + Style.RESET_ALL)
        
        #printing questions
        for idx, question in enumerate(SECURITY_QUESTIONS):
            print(f"{idx + 1 }.{question}")
        
        #user selects 3 questions from above list (stored as indexes)
        selected_indexes = []
        while len(selected_indexes) < 3: 
            try:
                choice = int(input(Fore.LIGHTYELLOW_EX + f"Choose Question {len(selected_indexes) + 1 }: " + Style.RESET_ALL)) - 1
                if 0 <= choice < len(SECURITY_QUESTIONS) and choice not in selected_indexes:
                    selected_indexes.append(choice)
                else:
                    print(Fore.RED + "❌ Invalid choice or already selected. Try again." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "❌ Invalid input! Please enter a number between 1 and 9." + Style.RESET_ALL)
        
        #getting the answers and hashing them
        answers = []
        for idx in selected_indexes:
            answer = input(Fore.LIGHTYELLOW_EX + f"Answer for {SECURITY_QUESTIONS[idx] }:" + Style.RESET_ALL).strip()
            hashed_answer = bcrypt.hashpw(answer.encode(),bcrypt.gensalt()).decode() #hashing the answer
            answers.append(hashed_answer)
        
        cursor.execute("""UPDATE admin 
                  SET ques_1 = %s, ques_2 = %s, ques_3 = %s, ans_1 = %s, ans_2 = %s, ans_3 = %s 
                  WHERE username = %s""",
               (*selected_indexes, *answers, username))
        cursor.connection.commit()

        
        print(Fore.LIGHTGREEN_EX + f"\n✅ Security questions updated successfully." + Style.RESET_ALL)
        

#-----------------------------------------------------------------------------------------------------
# STATIC METHOD TO UPDATE SECURITY QUESTIONS FOR EXISTING STUDENT USER
#-----------------------------------------------------------------------------------------------------
    @staticmethod
    def student_update_security_questions(cursor, email=None,phone=None):
        
        print(Fore.LIGHTYELLOW_EX + "Select 3 questions from below list of questions: " + Style.RESET_ALL)
        
        #printing questions
        for idx, question in enumerate(SECURITY_QUESTIONS):
            print(f"{idx + 1 }.{question}")
        
        #user selects 3 questions from above list (stored as indexes)
        selected_indexes = []
        while len(selected_indexes) < 3: 
            try:
                choice = int(input(Fore.LIGHTYELLOW_EX + f"Choose Question {len(selected_indexes) +1 }: " + Style.RESET_ALL)) - 1
                if 0 <= choice < len(SECURITY_QUESTIONS) and choice not in selected_indexes:
                    selected_indexes.append(choice)
                else:
                    print(Fore.RED + "❌ Invalid choice or already selected. Try again." + Style.RESET_ALL)
            except ValueError:
                input(Fore.RED + "❌ Invalid input! Please enter a number - between 1 and 9." + Style.RESET_ALL)
        
        #getting the answers and hashing them
        answers = []
        for idx in selected_indexes:
            answer = input(Fore.LIGHTYELLOW_EX + f"Answer for {SECURITY_QUESTIONS[idx] }:" + Style.RESET_ALL).strip()
            hashed_answer = bcrypt.hashpw(answer.encode(),bcrypt.gensalt()) #hashing the answer
            answers.append(hashed_answer)
        
        if email != None:
            cursor.execute("""UPDATE users 
                  SET ques_1 = %s, ques_2 = %s, ques_3 = %s, ans_1 = %s, ans_2 = %s, ans_3 = %s 
                  WHERE email = %s""",
               (*selected_indexes, *answers, email))
            cursor.connection.commit()
        elif phone != None:
             cursor.execute("""UPDATE users 
                  SET ques_1 = %s, ques_2 = %s, ques_3 = %s, ans_1 = %s, ans_2 = %s, ans_3 = %s 
                  WHERE phone = %s""",
               (*selected_indexes, *answers, phone))
             cursor.connection.commit()
        print(Fore.LIGHTGREEN_EX + f"\nAnswers updated successfully." + Style.RESET_ALL)
        
    #Screen Clearing Method
    @staticmethod
    def clear_screen():
        """Clears the console screen based on OS."""
        os.system("cls" if os.name == "nt" else "clear")
    
        
    
    
    
    