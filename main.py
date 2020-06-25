#!/usr/bin/env python3
import os
from checksumdir import dirhash
import sqlite3
import shutil
import time


FILE_PATH = './dirs.txt'
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
folders = dict()
DEST = '/home/muhia/Documents/saves/'


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

def copy_to_hardisk(conn,foldername, propername):
    
    if os.path.exists(DEST+propername):
        shutil.rmtree(DEST+propername)
        shutil.copytree(foldername,DEST+propername)
        update_database_item(conn,dirhash(foldername), foldername)
        print(f'Folder backup updated')
    else:
        print('folder is not backed up')

def update_database_item(conn, new_hashval, foldername):
    sql = """UPDATE savegames  SET id = ?, hashval = ? WHERE folder = ?"""
    cur = conn.cursor()
    cur.execute(sql, (new_hashval,new_hashval, foldername))


def check_hash_diff_change(conn, foldername, hashval):
    cursor = conn.cursor()
    cursor.execute("SELECT id, folder FROM savegames")
    rows = cursor.fetchall()
    folders = [{'id' : item[0],'foldername' : item[1]} for item in rows]

    for folder in folders:
        if folder['foldername'] == foldername:
            if folder['id'] == hashval:
                print(f'Folder {foldername} has not changed')
                return False
            else:
                print(f'Folder {foldername} has changed')
                return True



with db_connect(DEFAULT_PATH) as conn:
    create_database(conn)
    
    with open(FILE_PATH, 'r') as reader:
        line = reader.readline()
        while line != '':
            foldername = line.rstrip()
            namme = foldername.split('/')
            if(os.path.isdir(foldername)):
                dir_hashvalue = dirhash(foldername)
                
                if check_if_folder_in_database(conn, foldername) == False:
                    print(f'Adding folder {foldername} to database ')
                    
                    if os.path.exists(DEST+namme[len(namme)-1]):
                        shutil.rmtree(DEST+namme[len(namme)-1])
                        shutil.copytree(foldername, DEST+namme[len(namme)-1])
                    else:
                        shutil.copytree(foldername, DEST+namme[len(namme)-1])

                    
                    create_folder(conn, foldername, dir_hashvalue)
                else:
                    if check_hash_diff_change(conn, foldername, dir_hashvalue) == True:
                        copy_to_hardisk(conn, foldername, namme[len(namme)-1])
                    else:
                        pass

            else:
                print(f'{foldername} folder Does not exists')

            line = reader.readline()
            
            time.sleep(1)