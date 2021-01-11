import sqlite3
from sqlite3 import Error

import os
from datetime import datetime
import engine.generalfunction as fn

def create_connection(db_file):      
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def conn_error_handle():
    print("Error! System cannot connect to database now.")

def create_db(db_file):      
    conn = create_connection(db_file)
    if conn is not None:
        create_table_users(conn)
        create_table_offense(conn)
        create_table_account(conn)
    else:
        conn_error_handle()
         
def create_table_users(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE users (
                id             INTEGER PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
                surname        STRING  NOT NULL,
                firstname      STRING,
                othername      STRING,
                biodata        STRING,                
                dob            TEXT,
                marital_status STRING,
                is_deleted     INT     DEFAULT (0),
                date_created   TEXT
            );"""    
    cur.execute(sql)

def create_table_offense(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE offense (
                id             INTEGER         PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
                user_id        INTEGER          NOT NULL,
                date_committed TEXT,
                details        STRING,
                date_created TEXT,
                is_deleted                     DEFAULT (0) 
            );"""
    cur.execute(sql)
#added

#this functions has been modified

def create_table_account(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE account (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT    DEFAULT Admin,
        password TEXT    DEFAULT Admin
    );"""
    cur.execute(sql)

    create_default_account(conn)



def create_default_account(conn):
    name = 'Admin'
    password = 'Admin'
    data = (name,password)
    sql = ''' INSERT INTO account(name,password)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

#end

def create_users(conn, data):
    sql = ''' INSERT INTO users(surname,firstname,othername,marital_status,dob,biodata,date_created)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

def update_users(conn, data):
    sql = ''' UPDATE users
              SET surname = ? ,
                  firstname = ? ,
                  othername = ? ,
                  biodata = ?,
                  marital_status = ?,
                  dob = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def delete_users(conn, id):
    sql = '''DELETE FROM users 
                WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

    #Delete user images from dataset
    delete_user_images(id)
    delete_offence(conn,id)

def delete_user_images(id):
    print('deleting images...')
    i = 0
    while(i < 100):
        i +=1
        path = "data_images/User." + str(id) + '.' + str(i) + ".jpg"
        if os.path.exists(path):
            os.remove(path)
        else:
            print(str(i - 1) + ' images deleted')
            return

def delete_offence(conn, user_id):
    sql = '''DELETE FROM offense 
                WHERE user_id=?'''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    conn.commit()


def create_offense(conn, data):   
    sql = ''' INSERT INTO offense(user_id,details,date_committed,date_created)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

def get_users(conn, id):
    sql = "SELECT * FROM users WHERE id = ?"
    results = conn.execute(sql, (id,))
    return results

def get_offense(conn, user_id):
    sql = "SELECT * FROM offense WHERE user_id = ?"
    results = conn.execute(sql, (user_id,))
    return results

def get_account(conn):
    sql = "SELECT * FROM account"
    results = conn.execute(sql)
    return results

#added
def get_users_by_name(conn, name):    
    cursor = conn.cursor()
    if(not name):
        sql = "SELECT * FROM users"
        cursor.execute(sql)
    else:
        param = (name,name,name)
        sql = "SELECT * FROM users WHERE surname LIKE ? OR firstname LIKE ? OR othername LIKE ?"
        cursor.execute(sql, param)
    results = cursor.fetchall()
    return results

def update_account(conn, password):
    data = (password, 'user')
    sql = ''' UPDATE account
              SET password = ? ,
                  name = ?
              WHERE id = 1'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def update_account_change_user(conn, user_type):
    data = (user_type, 1)
    sql = ''' UPDATE account
              SET name = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

