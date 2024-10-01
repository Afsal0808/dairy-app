import os
import getpass
from cryptography.fernet import Fernet

# Function to generate or load encryption key
def load_key():
    try:
        if not os.path.exists('secret.key'):
            print("Generating a new encryption key...")
            key = Fernet.generate_key()
            with open('secret.key', 'wb') as key_file:
                key_file.write(key)
        else:
            print("Loading existing encryption key...")
            with open('secret.key', 'rb') as key_file:
                key = key_file.read()
        return key
    except Exception as e:
        print(f"Error loading key: {e}")
        exit(1)

# Function to encrypt data
def encrypt_data(data, key):
    try:
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data
    except Exception as e:
        print(f"Error encrypting data: {e}")
        return None

# Function to decrypt data
def decrypt_data(data, key):
    try:
        f = Fernet(key)
        decrypted_data = f.decrypt(data).decode()
        return decrypted_data
    except Exception as e:
        print(f"Error decrypting data: {e}")
        return None

# Login function for basic authentication
def login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")  # Hides password input
    
    if username == "admin" and password == "password":
        print("Login successful!")
        return True
    else:
        print("Login failed. Try again.")
        return False

# Function to add a diary entry
def add_entry(key):
    entry = input("Write your diary entry: ")
    encrypted_entry = encrypt_data(entry, key)
    
    if encrypted_entry:
        with open("diary.txt", "ab") as file:
            file.write(encrypted_entry + b"\n")
        print("Your entry has been saved securely!")
    else:
        print("Failed to save your entry.")

# Function to view diary entries
def view_entries(key):
    if os.path.exists("diary.txt"):
        try:
            with open("diary.txt", "rb") as file:
                lines = file.readlines()
                if lines:
                    print("Your diary entries:")
                    for line in lines:
                        decrypted_entry = decrypt_data(line.strip(), key)
                        if decrypted_entry:
                            print("-" * 40)
                            print(decrypted_entry)
                        else:
                            print("Failed to decrypt an entry.")
                else:
                    print("No entries found in the diary.")
        except Exception as e:
            print(f"Error reading diary entries: {e}")
    else:
        print("No diary entries found.")

# Main application function
def diary_app():
    print("Welcome to the Personal Diary App!")
    
    # Load encryption key
    key = load_key()
    
    if login():
        while True:
            print("\n1. Add Diary Entry")
            print("2. View Diary Entries")
            print("3. Exit")
            choice = input("Choose an option: ")
            
            if choice == '1':
                add_entry(key)
            elif choice == '2':
                view_entries(key)
            elif choice == '3':
                print("Exiting the app. Goodbye!")
                break
            else:
                print("Invalid option. Please choose again.")

# Run the diary app
if __name__ == "__main__":
    diary_app()
