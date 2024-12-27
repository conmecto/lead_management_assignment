import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)  
    return hashed_pw.decode('utf-8') 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_day_of_week(day: int) -> str:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[day]