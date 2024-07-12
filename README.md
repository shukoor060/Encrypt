# **File Encryption and Decryption Using User Passphrase**

![Intel Logo](https://logodownload.org/wp-content/uploads/2014/04/intel-logo-5-1.png)

## **Project Overview**

This project involves developing an application for file encryption, protected by a user passphrase. The main features include encrypting a user-chosen file or directory, securely storing the encryption key, and allowing decryption only upon successful passphrase authentication.

## **Table of Contents**

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Technical Details](#technical-details)
- [Testing](#testing)
- [Learning Outcomes](#learning-outcomes)
- [Contributors](#contributors)

## **Features**

- Encrypt a file using AES-256 encryption.
- Securely store the encryption key protected by a user passphrase.
- Decrypt the file only upon successful passphrase authentication.
- Securely delete original and encrypted files to prevent unauthorized access.
- Error handling for various edge cases like file not found, permission denied, etc.

## **Installation**

### **Prerequisites**

- Python 3.6 or above
- Required Python libraries:
  - `cryptography`


### **Steps**

1. **Clone the repository:**

    ```bash
    https://github.com/shukoor060/Encrypt.git
    cd project-repo
    ```

2. **Install the required Python libraries:**

    ```bash
    pip install cryptography 
    ```

## **Usage**

1. **To Encrypt or Decrypt a File:**

    ```bash
    python encrypt.py
    ```

## **Directory Structure**

```plaintext
project-repo/
├── encrypt.py
├── hello.txt
├── hello.txt.enc
├── hello.txt.salt
├── README.md
```

## Technical Details

### Encryption Process

1. **Generate a Key from the Passphrase:**
    - A salt is generated using `os.urandom(16)` for added randomness.
    - A key is derived from the user-provided passphrase and the salt using the PBKDF2HMAC algorithm with SHA256 as the hash function.

2. **Create a Fernet Instance:**
    - A Fernet instance is created using the derived key. Fernet is a symmetric encryption method included in the `cryptography` library.

3. **Read the File to be Encrypted:**
    - The file to be encrypted (`hello.txt`) is read in binary mode.

4. **Encrypt the File Data:**
    - The file data is encrypted using the Fernet instance.

5. **Write the Encrypted Data:**
    - The encrypted data is written to a new file (`hello.txt.enc`).

6. **Store the Salt:**
    - The salt used for key derivation is stored in a separate file (`hello.txt.salt`).

7. **Securely Delete the Original File:**
    - The original file (`hello.txt`) is securely deleted by overwriting it with random data before deletion.

### Decryption Process

1. **Retrieve the Stored Salt:**
    - The salt used during the encryption process is stored in a separate file (`hello.txt.salt`).
    - Read this salt from the file to ensure the same key can be derived from the passphrase.

2. **Generate the Key:**
    - Use the retrieved salt and the user-provided passphrase to generate the encryption key.
    - The key derivation is performed using the PBKDF2HMAC algorithm with SHA256 as the hash function.

3. **Create Fernet Instance:**
    - Create a Fernet instance using the derived key. Fernet is a symmetric encryption method included in the `cryptography` library.

4. **Read the Encrypted Data:**
    - Read the encrypted data from the encrypted file (`hello.txt.enc`).

5. **Decrypt the Data:**
    - Use the Fernet instance to decrypt the encrypted data.

6. **Write the Decrypted Data:**
    - Write the decrypted data back to the original file (`hello.txt`).

7. **Securely Delete Encrypted and Salt Files:**
    - Securely delete the encrypted file and the salt file to ensure they cannot be used to access the data in the future.
    - Overwrite these files with random data before deletion to prevent data recovery.

## How to Run

1. **Install Dependencies:**
    - Ensure you have `cryptography` library installed. You can install it using:
      ```sh
      pip install cryptography
      ```

2. **Encrypt a File:**
    - Run the script and choose to encrypt the file by providing the passphrase:
      ```sh
      python encrypt.py
      ```
    - Follow the prompts to enter your passphrase and encrypt the file.

3. **Decrypt a File:**
    - Run the script and choose to decrypt the file by providing the same passphrase:
      ```sh
      python encrypt.py
      
    - Follow the prompts to enter your passphrase and decrypt the file.

## Requirements
- Python 3.x
- `cryptography` library

## Contact
For any questions or issues, please contact Shukoor at developer.shukoor@gmail.com.
