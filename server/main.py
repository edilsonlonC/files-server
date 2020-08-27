#!/home/edilson/anaconda3/bin/python3.8
import zmq
import pickle
import json
import os
from database import (
    create_user,
    get_user,
    get_users_and_pass,
    get_file,
    create_file,
    get_files_by_owner_and_filename,
    get_files_by_owner,
)

# from database.connection import connection
from getpass import getpass
from utilities import get_filename, get_files_same_name, get_possible_name


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def register(info_user):
    username = info_user.get("username")
    password = info_user.get("password")
    # conn = connection()
    user = get_user(username)
    if not user:
        create_user(username, password)
        socket.send(pickle.dumps({"user_saved": True}))
    else:
        socket.send(pickle.dumps({"user_saved": False}))

def rewrite (id_user,filename,bytes_to_save):
    files_db = get_files_by_owner_and_filename(filename,id_user)
    name_to_save = get_filename(files_db[0][0], filename)
    with open(f"files/{name_to_save}", "wb") as f:
        f.write(bytes_to_save)
    socket.send(pickle.dumps({"file_saved": True}))




def uplodad_file(files):
    filename = files.get("filename")
    bytes_to_save = files.get("bytes")
    username = files.get("username")
    password = files.get("password")
    user = get_users_and_pass(username, password)
    if not user:
        socket.send(pickle.dumps({"unauthorized": True}))
        return
    if get_files_by_owner_and_filename(filename, user[0][0]):
        if files.get('rewrite'):
            rewrite(user[0][0] , filename,files.get('bytes'))
            return
        new_name = get_possible_name(filename)
        files['newname'] = new_name
        print(new_name)
        socket.send(pickle.dumps(files))
        return
    create_file(user[0][0], filename)
    file_in_db = get_files_by_owner_and_filename(filename, user[0][0])
    name_to_save = get_filename(file_in_db[0][0], filename)
    with open(f"files/{name_to_save}", "wb") as f:
        f.write(bytes_to_save)
    socket.send(pickle.dumps({"file_saved": True}))


def list_files(files):
    username = files.get("username")
    password = files.get("password")
    user = get_users_and_pass(username, password)
    if not user:
        socket.send(pickle.dumps({"unauthorized": True}))
        return
    files_in_db = get_files_by_owner(user[0][0])
    if not files_in_db:
        files_in_db = [(0, "no tiene elementos")]
    files_list = os.listdir("files")
    list_to_send = list(map(lambda filename: filename[1].encode("utf-8"), files_in_db))
    socket.send_multipart(list_to_send)


def download(files):
    username = files.get("username")
    password = files.get("password")
    filename = files.get("filename")
    user = get_users_and_pass(username, password)
    if not user:
        socket.send(pickle.dumps({"unauthorized": True}))
        return
    files_db = get_files_by_owner_and_filename(filename, user[0][0])
    download_info = {"filename": filename}
    if not files_db:
        download_info["fileNotFound"] = True
        socket.send(pickle.dumps(download_info))
        return
    name_in_folder = get_filename(files_db[0][0], filename)
    try:
        file = open(f"files/{name_in_folder}", "rb")
        bytes_to_download = file.read()
        download_info["bytes"] = bytes_to_download
        socket.send(pickle.dumps(download_info))
    except FileNotFoundError:
        print("error")
        download_info["fileNotFound"] = True
        socket.send(pickle.dumps(download_info))


def commands(files):
    command = files.get("command")
    if command == b"upload":
        files["filename"] = files.get("filename").decode("utf-8")
        files["bytes"] = files.get("bytes")
        uplodad_file(files)
    elif command == b"list":
        list_files(files)
    elif command == b"download":
        files["filename"] = files.get("filename").decode("utf-8")
        download(files)
    elif command == b"register":
        register(files)


def main():
    while True:
        print("server is running")
        message = socket.recv()
        files = pickle.loads(message)
        commands(files)


if __name__ == "__main__":

    main()
