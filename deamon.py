
from datetime import datetime
import threading
import time
import sqlite3
import os
from sys import exit, stderr

DATABASE = "/home/dnf/eNV/rustVenvs/backup/backup.db"


def start_backup():
    print("Starting backup")


def f_deamon():
    while True:
        now = datetime.now()
        sys_time = now.strftime("%H:%M")

        try:
            connection = sqlite3.connect(DATABASE)
        except sqlite3.Error as e:
            print(f"Something went wrong with the connection:\n{e}")
        else:
            cursor = connection.cursor()
            query = '''
            SELECT time FROM time WHERE time = ?
            '''
            cursor.execute(query, (sys_time,))
            results = cursor.fetchall()
            print(results)
            cursor.close()
            connection.close()
            start_backup()
            time.sleep(60)


if not os.path.exists(DATABASE):
    print("Error: No database found", file=stderr)
    exit(1)


thread1 = threading.Thread(target=f_deamon, daemon=False)
# Start backup process after some time
backup_thread = threading.Thread(target=start_backup,daemon=True)
thread1.start()

