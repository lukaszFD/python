import secrets
import string

def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    """
    # Define alphabet: letters, digits, and some punctuation
    alphabet = string.ascii_letters + string.digits + "!@#-$%^&*"

    # Securely choice characters from alphabet
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token

if __name__ == "__main__":
    # Example: you decide the length here
    user_length = 65
    new_token = generate_secure_token(user_length)

    print(f"Generated Token ({user_length} chars): {new_token}")