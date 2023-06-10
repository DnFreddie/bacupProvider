from cryptography.fernet import Fernet
import os 
import datetime as dt 
import sqlite3
DATABASE = "/home/dnf/eNV/rustVenvs/backup/backup.db"

def connect_db(key, time):
    create_db = '''
     CREATE TABLE IF NOT EXISTS encryption_keys (
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                key BLOB,
                time DATETIME
    )
    '''
    query = '''
    INSERT INTO encryption_keys (key, time)
    VALUES (?, ?)
    '''

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(create_db)
    cursor.execute(query, (key, time))
    connection.commit()
    connection.close()

    
def encrypt(files_encrypt, key_file):
    with open(key_file, 'rb') as file:
        key = file.read()

    encryption = Fernet(key)
    for file_encrypt in files_encrypt:
        with open(file_encrypt, "rb+") as file:
            data = file.read()
            encrypted_data = encryption.encrypt(data)
            file.seek(0)
            file.write(encrypted_data)
            file.truncate()





# Get the hold weather the files acctually exist 
backup_folder_path = os.path.expanduser("~/.encrypted_backup")

key_file = os.path.expanduser("~/.key_file")


if not os.path.exists(backup_folder_path):
    os.mkdir(backup_folder_path)

if not os.path.exists(key_file):
    current_datetime = dt.datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M")
    formatted_datetime = formatted_date + " " + formatted_time
    new_key = Fernet.generate_key()
    with open(key_file,'wb') as file:
        file.write(new_key)
    connect_db(new_key,formatted_datetime)
    for root, dirs, files in os.walk(backup_folder_path, topdown=True):
        file_paths = [os.path.join(root, file) for file in files]
        encrypt(file_paths, key_file)
else:
    
    for root, dirs, files in os.walk(backup_folder_path, topdown=True):
        file_paths = [os.path.join(root, file) for file in files]
        encrypt(file_paths, key_file)
