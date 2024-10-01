import os
import getpass
from cryptography.fernet import Fernet
def load_key():
    if not os.path.exists('secret.key'):
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
    else:
        with open('secret.key', 'rb') as key_file:
            key = key_file.read()
    return key
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data
def decrypt_data(data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(data).decode()
    return decrypted_data
def login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if username == "admin" and password == "password":
        print("Login successful!")
        return True
    else:
        print("Login failed. Try again.")
        return False
def add_entry(key):
    entry = input("Write your diary entry: ")
    encrypted_entry = encrypt_data(entry, key)
    with open("diary.txt", "ab") as file:
        file.write(encrypted_entry + b"\n")
    print("Your entry has been saved securely!")
def view_entries(key):
    if os.path.exists("diary.txt"):
        with open("diary.txt", "rb") as file:
            lines = file.readlines()
            print("Your diary entries:")
            for line in lines:
                decrypted_entry = decrypt_data(line.strip(), key)
                print("-" * 40)
                print(decrypted_entry)
    else:
        print("No diary entries found.")
def diary_app():
    print("Welcome to the Personal Diary App!")
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
