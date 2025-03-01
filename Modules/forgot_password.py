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
from dotenv import load_dotenv

class ForgotPassword:
#----------------------------------------------------------------------------------------------------------------------------
    #Forgot password FUNCTION
#----------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def forgot_password(cls):
        """Handles login logic for Admin and Student."""
        try:
            load_dotenv()
            conn = pymysql.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            cursor = conn.cursor()
            attempts = 0
            max_attempts = 3
            while attempts < max_attempts:
                cls.clear_screen()
                print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
                print(Fore.GREEN + "--------------------FORGOT PASSWORD------------------" + Style.RESET_ALL)
                print(Fore.CYAN + "=====================================================" + Style.RESET_ALL)
                print(Fore.LIGHTCYAN_EX + "Who are you, Please choose from below options" + Style.RESET_ALL)
                print(Fore.LIGHTCYAN_EX + "1. Admin" + Style.RESET_ALL)
                print(Fore.LIGHTCYAN_EX + "2. Student" + Style.RESET_ALL)
                print(Fore.LIGHTCYAN_EX + "3. Exit" + Style.RESET_ALL)
                
                try:
                    choice = int(input(Fore.LIGHTYELLOW_EX + "Enter your choice: " + Style.RESET_ALL))
                except ValueError:
                    input(Fore.RED + "❌ Invalid input! Please enter a valid number." + Style.RESET_ALL)
                    continue
                
                #ADMIN FORGOT PASSWORD LOGIC
                if choice == 1:
                    
                    #making sure username is not empty
                    while True:
                        username = input(Fore.LIGHTYELLOW_EX + "Please Enter your username: " + Style.RESET_ALL).strip()
                        if username:
                            break
                        else:
                            print(Fore.RED + "❌ Username cannot be empty! Please try again." + Style.RESET_ALL)

                    
                    #checking if the user exists in admin table or not, else prompt it to go back main menu and register himself/herself
                    cursor.execute("SELECT name FROM admin WHERE username = %s ",(username,))
                    result = cursor.fetchone()
                    if result:
                        print(Fore.LIGHTGREEN_EX + f"\n✅ User exists!!, please answer your security questions to reset password." + Style.RESET_ALL)
                        cursor.execute("SELECT ques_1,ques_2,ques_3,ans_1,ans_2,ans_3 FROM admin WHERE username = %s ",(username,))
                        security_ques_ans= cursor.fetchone()
                        
                        #Unpacking
                        ques_1_idx, ques_2_idx, ques_3_idx, ans_1, ans_2, ans_3 = security_ques_ans
                        
                        # Ask security questions
                        security_ans_1 = input(Fore.LIGHTBLUE_EX + f"1. {SECURITY_QUESTIONS[ques_1_idx]}: " + Style.RESET_ALL).strip()
                        security_ans_2 = input(Fore.LIGHTBLUE_EX + f"2. {SECURITY_QUESTIONS[ques_2_idx]}: " + Style.RESET_ALL).strip()
                        security_ans_3 = input(Fore.LIGHTBLUE_EX + f"3. {SECURITY_QUESTIONS[ques_3_idx]}: " + Style.RESET_ALL).strip()
                        
                        #Check Hashed password
                        if (bcrypt.checkpw(security_ans_1.encode(),ans_1.encode()) and 
                            bcrypt.checkpw(security_ans_2.encode(),ans_2.encode()) and 
                            bcrypt.checkpw(security_ans_3.encode(),ans_3.encode())):
                            
                            print(Fore.GREEN + "✅ All answers were correct, you can reset your password now!" + Style.RESET_ALL)
                            # Password validation
                            # Feature: need to implement password policy
                            while True:
                                new_user_password = input(Fore.LIGHTMAGENTA_EX + "Set New password: "+ Style.RESET_ALL).strip()
                                cursor.execute("SELECT password FROM admin WHERE username = %s ",(username,))
                                existing_password = cursor.fetchone()
                                if bcrypt.checkpw(new_user_password.encode(),existing_password[0].encode()):
                                    print(Fore.RED + "❌ New password cannot be the same as the old password. " + Style.RESET_ALL)
                                    print(Fore.RED + "Please enter a different password...." + Style.RESET_ALL)
                                    continue
                                re_enter_password = input(Fore.LIGHTMAGENTA_EX + "Confirm New password: "+ Style.RESET_ALL).strip()
                                if new_user_password == re_enter_password:
                                    break
                                else:
                                    input("❌ Passwords didn't match! Please try again."+ Style.RESET_ALL)
                            
                            hashed_password = bcrypt.hashpw(new_user_password.encode(), bcrypt.gensalt())
                            cursor.execute("""UPDATE admin SET password = %s WHERE username = %s """,(hashed_password.decode(),username))
                            conn.commit()
                            print(Fore.GREEN + "✅ Password reset successfully!" + Style.RESET_ALL)
                            time.sleep(3)
                        else:
                            attempts += 1
                            print(Fore.RED + f"❌ Answers didn't match! Attempts left: {max_attempts - attempts}" + Style.RESET_ALL)
                            input(Fore.LIGHTBLUE_EX + "Press Enter to try again..." + Style.RESET_ALL)  # Pause before returning to main menu
                    else:
                        attempts += 1
                        print(Fore.RED + f"❌ Admin User not found." + Style.RESET_ALL)
                        input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to main menu
                
                #STUDENT FORGOT PASSWORD LOGIC
                elif choice == 2:
                    #making sure username is not empty
                    email = None
                    phone = None
                    while True:
                        print(Fore.LIGHTCYAN_EX + "Please choose one to start reseting your password" + Style.RESET_ALL)
                        print(Fore.LIGHTCYAN_EX + "1. Email" + Style.RESET_ALL)
                        print(Fore.LIGHTCYAN_EX + "2. Phone" + Style.RESET_ALL)
                        
                        try:
                            choice = int(input(Fore.LIGHTYELLOW_EX + "Enter your choice: " + Style.RESET_ALL))
                        except ValueError:
                            attempts +=1 
                            print(Fore.RED + f"❌Invalid input! Please enter a valid number." + Style.RESET_ALL)
                            input(Fore.RED + f"❌Reset Attempts left: {max_attempts - attempts}" + Style.RESET_ALL)
                            break
                        
                        if choice == 1:
                            
                            email = input(Fore.LIGHTYELLOW_EX + "Please Enter your Email: " + Style.RESET_ALL).strip()
                            if email:
                                #Feature: implement email validation later
                                break
                            else:
                                print(Fore.RED + "❌ Email cannot be empty! Please try again." + Style.RESET_ALL)
                                attempts +=1 
                                input(Fore.RED + f"❌Reset Attempts left: {max_attempts - attempts}" + Style.RESET_ALL)
                                break
                        elif choice == 2:
                            phone = input(Fore.LIGHTYELLOW_EX + "Please Enter your Phone: " + Style.RESET_ALL).strip()
                            if not phone.isdigit() or len(phone) < 10:
                                input(Fore.RED + "❌ Invalid phone number. Please enter a valid 10-digit number."+ Style.RESET_ALL)
                                attempts +=1 
                                input(Fore.RED + f"❌Reset Attempts left: {max_attempts - attempts}" + Style.RESET_ALL)
                                break
                            else:
                                pass
                    
                    #checking if the user exists in users table or not, else prompt it to go back main menu and register himself/herself
                    if email != None:
                        cursor.execute("SELECT name FROM users WHERE email = %s ",(email,))
                        result = cursor.fetchone()
                    elif phone != None:
                        cursor.execute("SELECT name FROM users WHERE phone = %s ",(phone,))
                        result = cursor.fetchone()
                    
                    if result:
                        print(Fore.LIGHTGREEN_EX + f"\n✅ User exists!!, please answer your security questions to reset password." + Style.RESET_ALL)
                        if email != None:
                            cursor.execute("SELECT ques_1,ques_2,ques_3,ans_1,ans_2,ans_3 FROM users WHERE email = %s ",(email,))
                            security_ques_ans= cursor.fetchone()
                        elif phone != None:
                            cursor.execute("SELECT ques_1,ques_2,ques_3,ans_1,ans_2,ans_3 FROM users WHERE phone = %s ",(phone,))
                            security_ques_ans= cursor.fetchone()
                        
                        #Unpacking
                        ques_1_idx, ques_2_idx, ques_3_idx, ans_1, ans_2, ans_3 = security_ques_ans
                        
                        # Ask security questions
                        security_ans_1 = input(Fore.LIGHTBLUE_EX + f"1. {SECURITY_QUESTIONS[ques_1_idx]}: " + Style.RESET_ALL).strip()
                        security_ans_2 = input(Fore.LIGHTBLUE_EX + f"2. {SECURITY_QUESTIONS[ques_2_idx]}: " + Style.RESET_ALL).strip()
                        security_ans_3 = input(Fore.LIGHTBLUE_EX + f"3. {SECURITY_QUESTIONS[ques_3_idx]}: " + Style.RESET_ALL).strip()
                        
                        #Check Hashed password
                        if (bcrypt.checkpw(security_ans_1.encode(),ans_1.encode()) and 
                            bcrypt.checkpw(security_ans_2.encode(),ans_2.encode()) and 
                            bcrypt.checkpw(security_ans_3.encode(),ans_3.encode())):
                            
                            print(Fore.GREEN + "✅ All answers were correct, you can reset your password now!" + Style.RESET_ALL)
                            
                            # Password validation
                            # Feature: need to implement password policy
                            while True:
                                new_user_password = input(Fore.LIGHTMAGENTA_EX + "Set New password: "+ Style.RESET_ALL).strip()
                                
                                if email != None:
                                    cursor.execute("SELECT password FROM users WHERE email = %s ",(email,))
                                    existing_password = cursor.fetchone()
                                elif phone != None:
                                    cursor.execute("SELECT password FROM users WHERE phone = %s ",(phone,))
                                    existing_password = cursor.fetchone()
                                
                                #checking existing password with newly entered password
                                if bcrypt.checkpw(new_user_password.encode(),existing_password[0].encode()):
                                    print(Fore.RED + "❌ New password cannot be the same as the old password. " + Style.RESET_ALL)
                                    print(Fore.RED + "Please enter a different password...." + Style.RESET_ALL)
                                    continue
                                
                                re_enter_password = input(Fore.LIGHTMAGENTA_EX + "Confirm New password: "+ Style.RESET_ALL).strip()
                                
                                if new_user_password == re_enter_password:
                                    break
                                else:
                                    input("❌ Passwords didn't match! Please try again."+ Style.RESET_ALL)
                            
                            hashed_password = bcrypt.hashpw(new_user_password.encode(), bcrypt.gensalt())
                            if email != None:
                                cursor.execute("""UPDATE users SET password = %s WHERE email = %s """,(hashed_password.decode(),email))
                                conn.commit()
                            elif phone != None:
                                cursor.execute("""UPDATE users SET password = %s WHERE phone = %s """,(hashed_password.decode(),phone))
                                conn.commit()
                            print(Fore.GREEN + "✅ Password reset successfully!" + Style.RESET_ALL)
                            time.sleep(3)
                        else:
                            attempts += 1
                            print(Fore.RED + f"❌ Answers didn't match! Attempts left: {max_attempts - attempts}" + Style.RESET_ALL)
                            input(Fore.LIGHTBLUE_EX + "Press Enter to try again..." + Style.RESET_ALL)  # Pause before returning to main menu
                    else:
                        attempts += 1
                        print(Fore.RED + f"❌ User not found." + Style.RESET_ALL)
                        input(Fore.LIGHTBLUE_EX + "Press Enter to continue..." + Style.RESET_ALL)  # Pause before returning to main menu
                        
                elif choice == 3: 
                    print("Going back to home page.....")
                    input(Fore.LIGHTBLUE_EX  + "Press to continue...." + Style.RESET_ALL)
                    return
            
            if attempts >= max_attempts:
                print(Fore.RED + "❌ Too many failed attempts! Returning to main menu..." + Style.RESET_ALL)
                return
        
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
        
    #Screen Clearing Method
    @staticmethod
    def clear_screen():
        """Clears the console screen based on OS."""
        os.system("cls" if os.name == "nt" else "clear")

"""
Features to be implemented:

1. Extract Reusable Functions:
    You have repeated logic for checking user existence, security questions, and password resets for both Admins and Students. Move these into separate helper functions to improve readability and reduce redundancy.
2. Implement a Password Policy:
    Right now, any new password can be set as long as it differs from the old one. Consider enforcing a strong password policy, such as:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
3. Validate Email & Phone Properly:
    - The email format should be validated using regex.
    - Instead of len(phone) < 10, enforce an exact length of 10 digits and allow only numeric values.
4. Limit the Number of Attempts for Security Questions:
    - If security question answers are incorrect 3 times, consider locking the user out for a cooldown period.
5. Logging & Security
    - Store failed reset attempts in the database to prevent brute-force attacks.
    - Log password reset attempts for better security tracking.
"""