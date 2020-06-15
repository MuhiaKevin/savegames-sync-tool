def check_folder(conn, id=None):
    cursor = conn.cursor()
    rows = cursor.execute("SELECT id FROM savegames")
    
    print(rows)




    #!/usr/bin/env python3
import os
from checksumdir import dirhash
import sqlite3


"""
        https://pypi.org/project/checksumdir/1.0.5/
        https://stackoverflow.com/questions/24937495/how-can-i-calculate-a-hash-for-a-filesystem-directory-using-python
        https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3
        https://realpython.com/read-write-files-python/
        https://www.codecademy.com/articles/what-is-sqlite


        1. check if the directory exists
        2. if folder exists check if it is saved in the database
        2.  if folder exists and is in the database, calculate the sha256 and check if it the same as that in the sqlite database
        3. if it has changed then upload to cloud
        4, if it has not changed then leave it as it is
        5. if folder does not exist then throw error
"""

FILE_PATH = './dirs.txt'
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
folders = list()


def db_connect(db_path=DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    return connection


def create_folder(con, folder, hashval):
    sql = """
        INSERT INTO savegames (id, folder, hashval) VALUES (?, ?, ?)
    """
    cur = con.cursor()
    cur.execute(sql, (str(hashval),  str(folder), str(hashval)))
    return cur.lastrowid


def create_database(conn):
    cursor = conn.cursor()
    savegame_sql = "CREATE TABLE IF NOT EXISTS savegames (id TEXT PRIMARY KEY, folder TEXT NOT NULL, hashval TEXT NOT NULL)"
    cursor.execute(savegame_sql)


def check_if_folder_id_in_database(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM savegames")
    rows = cursor.fetchall()
    ids = list()
    print(rows)
    # use list compression and search how to enter contents of tuple to a list
    # for id in rows:
    #     ids.append(id[0])

    # if id not in ids:
    #     return False
    # else:
    #     return True


def folders(conn, folders):
    cursor = conn.cursor()
    cursor.execute("SELECT id, folder, hashval FROM savegames")
    rows = cursor.fetchall()
    print(rows)


with db_connect(DEFAULT_PATH) as conn:
    create_database(conn)

    with open(FILE_PATH, 'r') as reader:
        line = reader.readline()
        while line != '':
            foldername = line.rstrip()

            if(os.path.isdir(foldername)):
                dir_hashvalue = dirhash(foldername)

                if check_if_folder_id_in_database(conn, dir_hashvalue) ==  False:
                    print('Folder is in the database')
                
                elif  check_if_folder_id_in_database(conn, dir_hashvalue) == True:
                    print('Folder is not in the database')
                    create_folder(conn, foldername, dir_hashvalue)
                    print('Added folder to database')

                # print(f'{foldername} folder exists {dir_hashvalue}')
            # else:
            #     print(f'{foldername} folder Does not exists')

            line = reader.readline()

    # folders(conn, folders)