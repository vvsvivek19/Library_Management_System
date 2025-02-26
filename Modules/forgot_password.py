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
        input("To be implemented")
        
    #Screen Clearing Method
    @staticmethod
    def clear_screen():
        """Clears the console screen based on OS."""
        os.system("cls" if os.name == "nt" else "clear")