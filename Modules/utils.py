import re

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

def validate_password(password):
    validate = re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$",password)
    return(bool(validate))