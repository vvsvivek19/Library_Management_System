import time
import pymysql
import bcrypt 
import getpass
from library_management import Library,Book

class User:

    @classmethod
    def register(cls):
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
        
    @classmethod
    def login(cls):
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
            time.sleep(0.1)
            print("1. Login as Admin")
            time.sleep(0.1)
            print("2. Login as Student")
            time.sleep(0.1)
            print("3. Go back")
            
            try:
                choice = int(input("Are you a student or admin? Please choose from above: "))
            except ValueError:
                print("❌ Invalid input! Please enter a number (1, 2, or 3).")
                return
            
            #Loging in as a Admin logic
            if choice == 1:
                print("****************************************************")
                print("--------------------ADMIN LOGIN----------------------")
                username = input("Username: ").strip()
                password = getpass.getpass("Password: ").strip()
                cursor.execute("SELECT password, name FROM admin WHERE username = %s ",(username,))
                result = cursor.fetchone()
                if result:
                    stored_hashed_password = result[0].encode() # Convert stored password back to bytes
                    if bcrypt.checkpw(password.encode(),stored_hashed_password):
                        print(f"\n✅ Welcome {result[1]}! You are logged in as an admin.")
                        print("What do wanna do? Please choose from below\n")
                        print("1. Add a book\n")
                        print("2. Remove a book\n")
                        print("3. Search a book\n")
                        print("4. Display Available books\n")
                        print("5. Update book details\n")
                        print("6. Borrow a book as a admin\n")
                        print("7. Return a book as a admin\n")
                        print("8. See borrow history of a user\n")
                        print("9. Fine Calculation\n")
                        print("10. Report Generation\n")
                        print("11. Remove a admin user (Super Admin Only)\n")
                    else:
                        print("❌ Incorrect password.")
                else:
                    print("❌ Admin User not found.")
            
            #Loging in as a student logic
            elif choice == 2:
                pass
            
            #Going back logic
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
        
    
    
    
    