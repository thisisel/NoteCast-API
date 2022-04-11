from passlib.context import CryptContext


class PasswordManager:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def check_password_hash(cls, plain_password, password_hash):
        return cls.pwd_context.verify(plain_password, password_hash)

    @classmethod
    def generate_password_hash(cls, plain_password):
        return cls.pwd_context.hash(plain_password)

