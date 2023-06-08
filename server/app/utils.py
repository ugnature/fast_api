from passlib.context import CryptContext


# password hashing
pwd_hashing = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(user_password: str):
    return pwd_hashing.hash(user_password)


def verify(plain_password, hashed_password):
    return pwd_hashing.verify(plain_password, hashed_password)
