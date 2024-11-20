import pyzipper
import os
from password_cracking.password_mutations import generate_password_mutations


def brute_force_zip(zip_file, password_file):
    mutations = generate_password_mutations(password_file)  # Get password mutations

    # Open the ZIP file and check if it is encrypted
    try:
        with pyzipper.AESZipFile(zip_file, 'r') as z:
            print(f"Starting brute-force attack on the ZIP file: {zip_file}")

            # Try each mutation from the list
            for password in mutations:
                print(f"Trying password: {password}")
                try:
                    z.setpassword(password.encode('utf-8'))  # Set the current password
                    z.extractall()  # Try to extract the contents
                    print(f"Password found: {password}")
                    return
                except RuntimeError:
                    # Handle incorrect passwords
                    continue

            print("Password not found in the provided wordlist.")

    except (pyzipper.BadZipFile, RuntimeError) as e:
        print(f"Error with ZIP file: {e}")
        return


# Example usage:
base_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub")
password_file = os.path.join(base_path, "python", "passwords.txt")
zip_file = "example.zip"
brute_force_zip(zip_file, password_file)
