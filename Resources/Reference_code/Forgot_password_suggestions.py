# 1. Move Database Operations to a Separate Module
# Why? Separating concerns makes your code cleaner and reusable.

# How to Implement?

# Create a database.py file and define functions like get_user_by_username(), update_password(), etc.
# Replace direct cursor.execute() calls with function calls from database.py.
# Example (database.py):


# import pymysql

# def get_connection():
#     return pymysql.connect(host="localhost", user="root", password="Vivek1465", database="librarydb")

# def get_user_by_username(username, role):
#     conn = get_connection()
#     cursor = conn.cursor()
#     table = "admin" if role == "admin" else "users"
#     cursor.execute(f"SELECT * FROM {table} WHERE username = %s", (username,))
#     return cursor.fetchone()
# Then use:


# from Modules.database import get_user_by_username

# user = get_user_by_username(username, "admin")
# if user:
#     print("User found")
# 2. Implement a Strong Password Policy
# Why? To enforce security and prevent weak passwords.

# How to Implement?
# Use a function to validate passwords:


# import re

# def is_strong_password(password):
#     if (len(password) < 8 or 
#         not re.search(r"[A-Z]", password) or 
#         not re.search(r"[a-z]", password) or 
#         not re.search(r"[0-9]", password) or 
#         not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
#         return False
#     return True
# Call this function before accepting a new password:

# while True:
#     new_password = input("Set New Password: ").strip()
#     if is_strong_password(new_password):
#         break
#     else:
#         print("Password must be at least 8 characters long and include an uppercase letter, lowercase letter, number, and special character.")
# 3. Rate Limiting to Prevent Brute Force Attacks
# Why? Prevents users from trying unlimited attempts.

# How to Implement?
# Instead of using max_attempts, implement a timestamp-based lockout.

# import time

# failed_attempts = {}

# def is_locked_out(username):
#     if username in failed_attempts:
#         last_attempt, attempt_count = failed_attempts[username]
#         if attempt_count >= 3:
#             if time.time() - last_attempt < 300:  # 5-minute lockout
#                 return True
#             else:
#                 del failed_attempts[username]  # Reset after timeout
#     return False

# def record_failed_attempt(username):
#     if username in failed_attempts:
#         failed_attempts[username] = (time.time(), failed_attempts[username][1] + 1)
#     else:
#         failed_attempts[username] = (time.time(), 1)
# Call this before verifying the user:


# if is_locked_out(username):
#     print("Too many failed attempts! Please try again later.")
#     return
# 4. Use Environment Variables for Database Credentials
# Why? Hardcoded credentials (password="Vivek1465") are a security risk.

# How to Implement? Use dotenv to load environment variables.

# Install python-dotenv:
# pip install python-dotenv
# Create a .env file:

# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=Vivek1465
# DB_NAME=librarydb
# Modify your code:

# from dotenv import load_dotenv
# import os

# load_dotenv()
# conn = pymysql.connect(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME")
# )
# 5. Add Email or SMS-Based Password Reset (Optional)
# Why? Security questions can be guessed or socially engineered.

# How to Implement? Use an OTP system with an email service like SMTP or an SMS API.

# Example:

# import smtplib
# import random

# def send_otp(email):
#     otp = str(random.randint(100000, 999999))
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login("your_email@gmail.com", "your_email_password")
#     server.sendmail("your_email@gmail.com", email, f"Your OTP is {otp}")
#     return otp
# Then prompt the user to enter the OTP before resetting their password.

# 6. Improve Code Readability by Using More Helper Functions
# Why? Reduces redundancy.

# How to Implement?
# Instead of repeating security question logic, use a function:


# def verify_security_questions(cursor, username, role):
#     table = "admin" if role == "admin" else "users"
#     cursor.execute(f"SELECT ques_1,ques_2,ques_3,ans_1,ans_2,ans_3 FROM {table} WHERE username = %s", (username,))
#     security_ques_ans = cursor.fetchone()

#     if not security_ques_ans:
#         return False

#     ques_1_idx, ques_2_idx, ques_3_idx, ans_1, ans_2, ans_3 = security_ques_ans

#     # Ask security questions
#     for i, (ques_idx, ans) in enumerate(zip([ques_1_idx, ques_2_idx, ques_3_idx], [ans_1, ans_2, ans_3])):
#         security_ans = input(f"{i+1}. {SECURITY_QUESTIONS[ques_idx]}: ").strip()
#         if not bcrypt.checkpw(security_ans.encode(), ans.encode()):
#             return False
#     return True
# Then replace multiple lines of verification with:


# if verify_security_questions(cursor, username, "admin"):
#     print("✅ Answers correct, you may reset your password.")
# 7. Use Logging Instead of Print Statements
# Why? Logs help in debugging and security monitoring.

# How to Implement? Use Python’s logging module:


# import logging

# logging.basicConfig(filename="forgot_password.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# def log_attempt(username, success):
#     if success:
#         logging.info(f"Password reset successful for {username}")
#     else:
#         logging.warning(f"Failed password reset attempt for {username}")
# Replace print with log_attempt(username, success).

# Final Thoughts
# By implementing these improvements, your forgot password system will be: ✅ More secure
# ✅ Easier to maintain
# ✅ More user-friendly

# Which one do you want to start with first? 🚀