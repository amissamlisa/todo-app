import secrets
import string


def generate_secure_string(length=72):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))