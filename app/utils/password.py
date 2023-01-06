import bcrypt


def hash_password(password: str):
    """Hash password"""
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()


def check_password(password: str, hashed_password: str):
    """Check if password matches hashed password"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
