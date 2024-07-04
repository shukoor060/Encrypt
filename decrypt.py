import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

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

# Function to decrypt the FEK using the derived key
def decrypt_fek(encrypted_fek, passphrase):
    iv = encrypted_fek[:16]
    salt = encrypted_fek[16:32]
    encrypted_key = encrypted_fek[32:]

    derived_key = derive_key_from_passphrase(passphrase, salt)
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_key) + decryptor.finalize()

# Function to decrypt a file with the FEK
def decrypt_file(file_path, fek):
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(fek), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(file_path[:-4], 'wb') as f:  # Remove the '.enc' extension
        f.write(plaintext)
    os.remove(file_path)  # Remove the encrypted file after decryption

# Function to decrypt all files within the 'test' folder
def decrypt_folder(folder_path, passphrase):
    # Load the encrypted FEK
    with open(os.path.join(folder_path, 'folder.key'), 'rb') as f:
        encrypted_fek = f.read()

    # Decrypt the FEK
    fek = decrypt_fek(encrypted_fek, passphrase)

    # Decrypt each file in the folder
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.enc'):
                file_path = os.path.join(dirpath, filename)
                decrypt_file(file_path, fek)

    print("Folder decryption complete.")

def main():
    folder_path = "test"  # Folder name is 'test' and is in the same directory
    if not os.path.exists(folder_path):
        print("Folder 'test' does not exist in the current directory.")
        return

    passphrase = input("Enter the passphrase: ")

    # Decrypt the folder
    decrypt_folder(folder_path, passphrase)

    print(f"Decrypted folder: {folder_path}")

if __name__ == "__main__":
    main()
