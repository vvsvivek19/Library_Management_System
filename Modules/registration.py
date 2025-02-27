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


class Registration:
#----------------------------------------------------------------------------------------------------------------------------
    #REGISTER FUNCTION
#----------------------------------------------------------------------------------------------------------------------------
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
    
    
    