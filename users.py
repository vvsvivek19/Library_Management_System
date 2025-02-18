import time
import pymysql
import bcrypt 

class User:

    @classmethod
    def register(cls):
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
            print("Welcome to Central Library!!!")
            time.sleep(0.1)
            print("Whom do you want to register as?")
            time.sleep(0.1)
            print("1. Admin")
            time.sleep(0.1)
            print("2. Student")
            time.sleep(0.1)
            print("3. Go back")
            choice = int(input("Please choose from above options: "))
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
                        print(f"Welcome {result[1]}!!! ")
                    else:
                        print("❌ Incorrect password.")
                else:
                    print("❌ Admin User not found.")
                        
                    
        except pymysql.MySQLError  as err:
             print("❌ Error Occurred:", err)
        finally:
            # Close connection
            cursor.close()
            conn.close()
    
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
            print("1. Student")
            time.sleep(0.1)
            print("2. Admin")
            time.sleep(0.1)
            print("3. Go back")
            choice = int(input("Are you a student or admin? Please choose from below: "))
            if choice == 1:
                print("****************************************************")
                email = input("Email: ").strip()
                password = input("password: ").strip()
        except pymysql.MySQLError  as err:
             print("❌ Error Occurred:", err)
        finally:
            # Close connection
            cursor.close()
            conn.close()
    
    
    
    