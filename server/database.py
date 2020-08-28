import sqlite3

con = sqlite3.connect("./database.db")


def create_user(username, password):
    cursor = con.cursor()
    cursor.execute("INSERT INTO user (name , pass) values (?,?)", (username, password,))
    con.commit()


def get_users():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()
    return rows


def get_user(username):

    cursor = con.cursor()
    cursor.execute("SELECT id FROM user where name = ? ", (username,))
    rows = cursor.fetchall()
    return rows


def get_users_and_pass(username, password):

    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM user WHERE name = ? AND pass = ? ", (username, password)
    )
    rows = cursor.fetchall()
    return rows


def create_file(id_owner, filename):
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO files (namefile , id_owner) VALUES (?,?)", (filename, id_owner,)
    )
    con.commit()


def get_files_by_owner_and_filename(filename, id_owner):
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM files WHERE namefile = ? AND  id_owner = ? ",
        (filename, id_owner),
    )
    rows = cursor.fetchall()
    return rows


def get_file(filename):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM files WHERE  namefile = ? ", (filename,))
    rows = cursor.fetchall()
    return rows


def get_files_by_owner(id_owner):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM files WHERE id_owner = ? ", (id_owner,))
    rows = cursor.fetchall()
    return rows


def get_files():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM files")
    rows = cursor.fetchall()
    return rows


def get_files_same_name(filename,id_user):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM files WHERE namefile LIKE '%'||?||'%' and id_owner = ?" , (filename,id_user))
    rows = cursor.fetchall()
    return rows
