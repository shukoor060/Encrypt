import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Function to generate a random File Encryption Key (FEK)
def generate_fek():
    return os.urandom(32)  # Generate a 256-bit (32-byte) random key

# Function to derive a key from the passphrase using PBKDF2
def derive_key_from_passphrase(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(passphrase.encode())

# Function to encrypt a file with the FEK
def encrypt_file(file_path, fek):
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(fek), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(file_path + '.enc', 'wb') as f:
        f.write(iv + ciphertext)
    os.remove(file_path)  # Remove the original file after encryption

# Function to encrypt the FEK using the derived key
def encrypt_fek(fek, passphrase):
    salt = os.urandom(16)
    derived_key = derive_key_from_passphrase(passphrase, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_fek = encryptor.update(fek) + encryptor.finalize()
    return iv + salt + encrypted_fek

# Function to store the encrypted FEK
def store_encrypted_fek(encrypted_fek, path):
    with open(path, 'wb') as f:
        f.write(encrypted_fek)

# Function to encrypt all files within the 'test' folder
def encrypt_folder(folder_path, passphrase):
    fek = generate_fek()

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            encrypt_file(file_path, fek)

    encrypted_fek = encrypt_fek(fek, passphrase)
    store_encrypted_fek(encrypted_fek, os.path.join(folder_path, 'folder.key'))

    print("Folder encryption complete.")

def main():
    folder_path = "test"  # Folder name is 'test' and is in the same directory
    if not os.path.exists(folder_path):
        print("Folder 'test' does not exist in the current directory.")
        return

    passphrase = input("Enter a passphrase: ")

    # Encrypt the folder
    encrypt_folder(folder_path, passphrase)

    print(f"Encrypted folder: {folder_path}")

if __name__ == "__main__":
    main()
