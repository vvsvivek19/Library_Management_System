import bcrypt
import pymysql

# Database connection
conn = pymysql.connect(host="localhost", user="root", password="Vivek1465", database="librarydb")
cursor = conn.cursor()

# Generate a hashed default answer
default_answer = "DefaultAnswer123"
hashed_default_answer = bcrypt.hashpw(default_answer.encode(), bcrypt.gensalt())

# Assign random security questions to existing users
cursor.execute("SELECT admin_id FROM admin")
user_ids = cursor.fetchall()

for user_id in user_ids:
    selected_indexes = [0, 1, 2]  # You can modify this logic to select random questions
    print(f"Updating admin {user_id[0]} with security questions...")
    cursor.execute("""
        UPDATE admin 
        SET ques_1 = %s, ques_2 = %s, ques_3 = %s, ans_1 = %s, ans_2 = %s, ans_3 = %s
        WHERE admin_id = %s
    """, (*selected_indexes, hashed_default_answer, hashed_default_answer, hashed_default_answer, user_id[0]))

conn.commit()

print("✅ Security questions added for all existing users.")

cursor.close()
conn.close()
