import pyzipper

def unzip_with_password(zip_filename, password, output_dir):
    try:
        # Open the encrypted ZIP file
        with pyzipper.AESZipFile(zip_filename, mode='r', encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password.encode('utf-8'))  # Set the password for the zip file
            zipf.extractall(path=output_dir)  # Extract all files to the specified directory
            print(f"Files extracted successfully to {output_dir}")
    except RuntimeError as e:
        print(f"Failed to unzip the file: {e}")

# Example usage
unzip_with_password("example.zip", "NOvember2024", "./extracted_files")
