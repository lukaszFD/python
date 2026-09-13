import secrets
import string

def generate_vault_token(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

print(generate_vault_token(32))