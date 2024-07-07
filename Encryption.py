import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Constants for file names
FILE_NAME = "hello.txt"
ENCRYPTED_FILE_NAME = FILE_NAME + ".enc"
SALT_FILE_NAME = FILE_NAME + ".salt"

def generate_key_from_passphrase(passphrase, salt=None):
    """
    Generate a key from the given passphrase and salt using PBKDF2.
    If no salt is provided, generate a new random salt.
    """
    if salt is None:
        salt = os.urandom(16)  # Generate a new random salt
    
    # Create a key derivation function (KDF) instance
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    
    # Derive the key using the passphrase and KDF
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key, salt

def secure_delete(file_path):
    """
    Securely delete a file by overwriting it with random data before deletion.
    """
    if not os.path.exists(file_path):
        return

    # Get the file size
    file_size = os.path.getsize(file_path)
    
    # Overwrite the file with random data
    with open(file_path, "wb") as f:
        f.write(os.urandom(file_size))
    
    # Delete the file
    os.remove(file_path)

def encrypt_file(passphrase):
    """
    Encrypt the specified file using a passphrase. 
    Securely delete the original file after encryption.
    """
    try:
        # Generate a key from the passphrase
        key, salt = generate_key_from_passphrase(passphrase)
        
        # Create a Fernet instance for encryption
        fernet = Fernet(key)
        
        # Read the file content
        with open(FILE_NAME, 'rb') as file:
            file_data = file.read()
        
        # Encrypt the data
        encrypted_data = fernet.encrypt(file_data)
        
        # Write the encrypted data to a new file
        with open(ENCRYPTED_FILE_NAME, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        
        # Store the salt in a separate file
        with open(SALT_FILE_NAME, 'wb') as salt_file:
            salt_file.write(salt)
        
        # Securely delete the original file
        secure_delete(FILE_NAME)
        
        print(f"File '{FILE_NAME}' encrypted successfully and original securely deleted.")
    except FileNotFoundError:
        print(f"Error: The file '{FILE_NAME}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access '{FILE_NAME}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def decrypt_file(passphrase):
    """
    Decrypt the encrypted file using the provided passphrase.
    Securely delete the encrypted file and salt file after decryption.
    """
    try:
        # Read the salt from the salt file
        with open(SALT_FILE_NAME, 'rb') as salt_file:
            salt = salt_file.read()
        
        # Generate the key from the passphrase and salt
        key, _ = generate_key_from_passphrase(passphrase, salt)
        
        # Create a Fernet instance for decryption
        fernet = Fernet(key)
        
        # Read the encrypted data from the file
        with open(ENCRYPTED_FILE_NAME, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write the decrypted data back to the original file
        with open(FILE_NAME, 'wb') as file:
            file.write(decrypted_data)
        
        # Securely delete the encrypted file and salt file
        secure_delete(ENCRYPTED_FILE_NAME)
        secure_delete(SALT_FILE_NAME)
        
        print(f"File '{FILE_NAME}' decrypted successfully and encrypted version securely deleted.")
    except FileNotFoundError:
        print(f"Error: The encrypted file or salt file was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access the files.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    """
    Main function to handle user input for encrypting or decrypting a file.
    """
    while True:
        # Prompt the user to choose an action
        action = input("Enter 'e' to encrypt, 'd' to decrypt, or 'q' to quit: ").lower()
        
        if action == 'q':
            break
        elif action in ['e', 'd']:
            passphrase = input("Enter the passphrase: ")
            
            if action == 'e':
                encrypt_file(passphrase)
            else:
                decrypt_file(passphrase)
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()
