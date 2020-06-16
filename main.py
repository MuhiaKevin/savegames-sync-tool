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
folders = dict()


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
    savegame_sql = "CREATE TABLE IF NOT EXISTS savegames (id TEXT, folder TEXT NOT NULL, hashval TEXT NOT NULL)"
    cursor.execute(savegame_sql)

def folders(conn, folders):
    cursor = conn.cursor()
    cursor.execute("SELECT id, folder, hashval FROM savegames")
    print(cursor.fetchall())

def check_if_folder_in_database(conn, foldername):
    cursor = conn.cursor()
    cursor.execute("SELECT folder FROM savegames")
    rows = cursor.fetchall()
    folders = set()

    for iditem in rows:
        folders.add(iditem[0])

    if foldername not in folders:
        return False
    else:
        return True

def check_hash_diff(conn, foldername, hashval):
    cursor = conn.cursor()
    cursor.execute("SELECT id, folder FROM savegames")
    rows = cursor.fetchall()
    folders = [{'id' : item[0],'foldername' : item[1]} for item in rows]

    for folder in folders:
        if folder['foldername'] == foldername:
            if folder['id'] == hashval:
                print(f'Folder {foldername} has not changed')
            else:
                print(f'Folder {foldername} has changed')



with db_connect(DEFAULT_PATH) as conn:
    create_database(conn)
    
    with open(FILE_PATH, 'r') as reader:
        line = reader.readline()
        while line != '':
            foldername = line.rstrip()

            if(os.path.isdir(foldername)):
                dir_hashvalue = dirhash(foldername)
                
                if check_if_folder_in_database(conn, foldername) == False:
                    create_folder(conn, foldername, dir_hashvalue)
                else:
                    check_hash_diff(conn, foldername, dir_hashvalue)

                # print(f'{foldername} folder exists {dir_hashvalue}')
            # else:
            #     print(f'{foldername} folder Does not exists')

            line = reader.readline()