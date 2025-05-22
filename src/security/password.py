from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=['bcrypt']
)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_password(entered_password: str, db_password_hash: str) -> bool:
    return pwd_context.verify(entered_password, db_password_hash)
