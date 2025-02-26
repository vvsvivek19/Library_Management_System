'''
Importing Important modules - both native and external
'''
import time
import pymysql
import bcrypt 
import getpass
import os
from colorama import Fore, Style


class ForgotPassword:
#----------------------------------------------------------------------------------------------------------------------------
    #Forgot password FUNCTION
#----------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def forgot_password(cls):
        SECURITY_QUESTIONS = [
            "What is the name of your first pet?",
            "What was your childhood nickname?",
            "What is your mother's maiden name?",
            "What was the make of your first car?",
            "What is your favorite book?",
            "Where did you go to high school?",
            "What city were you born in?",
            "What is your favorite movie?",
            "What was your first job?"
        ]
        input("To be implemented")
        
    #Screen Clearing Method
    @staticmethod
    def clear_screen():
        """Clears the console screen based on OS."""
        os.system("cls" if os.name == "nt" else "clear")