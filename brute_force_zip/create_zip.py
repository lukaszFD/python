import pyzipper

def create_zip_with_password(zip_filename, files_to_zip, password):
    # Create a new ZIP file with AES encryption
    with pyzipper.AESZipFile(zip_filename, mode='w', encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password.encode('utf-8'))  # Set the password for the zip file
        for file in files_to_zip:
            zipf.write(file, arcname=file.split('/')[-1])  # Add files to the zip

    print(f"ZIP file '{zip_filename}' created with password protection.")

# Example usage
files = ["example.txt"]  # Replace with the paths to your files
create_zip_with_password("example.zip", files, "NOvember2024")
