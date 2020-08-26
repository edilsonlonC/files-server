import sqlite3

con = sqlite3.connect('database.db')


def create_user(username, password):
    cursor = con.cursor()
    cursor.execute('INSERT INTO user (name , pass) values (?,?)',(username,password,))
    con.commit()


def get_users():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM user')
    rows = cursor.fetchall()
    return rows

def get_user(username):
    cursor = con.cursor()
    cursor.execute('SELECT * FROM user where name = ? ' , (username,))
    rows = cursor.fetchall()
    return rows


def get_users_and_pass (username,password):
    cursor = con.cursor()
    cursor.execute('SELECT * FROM user where name = ? AND pass = ? ' , (username,password))
    rows = cursor.fetchall()
    return rows

def create_file(id_owner,filename):
    cursor = con.cursor()
    cursor.execute('INSERT INTO files (namefile , id_owner) values (?,?)', (filename, id_owner,))
    con.commit()

def get_files():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM files')
    rows = cursor.fetchall()
    return rows

