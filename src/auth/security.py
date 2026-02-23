from passlib.context import CryptContext


hash_context = CryptContext(schemes=["bcrypt"])


def get_hash(pswd: str):
    return hash_context.encrypt(pswd)


def verify_hash(s: str, hash: str):
    return hash_context.verify(s, hash)
