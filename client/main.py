#!/home/edilson/anaconda3/bin/python3.8

import zmq
import sys
import sys
import pickle
from utilities import generate_output_files
from colorama import Fore
from getpass import getpass

files = {}

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def send_register(info_user):
    info_to_send = pickle.dumps(info_user)
    print(info_to_send)
    socket.send(info_to_send)
    response = socket.recv()
    json_response = pickle.loads(response)
    if not json_response.get("user_saved"):
        username = info_user.get("username")
        print(f"username {username} exist")
        return
    print("user created")


def register(args):
    if len(args) < 2:
        print('arguments missed')
        return
    password = getpass()
    files["username"] = args[1]
    files["password"] = password
    print(files)
    send_register(files)


def upload(args):
    if len(args) < 4:
        print('arguments missed')
        return
    files["filename"] = args[1].encode("utf-8")
    files["username"] = args[2]
    files["password"] = args[3]
    try:
        file = open(files.get("filename"), "rb")
        if "/" in args[1]:
            files["filename"] = args[1].split("/")[-1].encode("utf-8")
            print(files.get("filename"))

        bytes_file = file.read()
        files["bytes"] = bytes_file
        socket.send(pickle.dumps(files))
        response = socket.recv()
        json_message = pickle.loads(response)
        if json_message.get("unauthorized"):
            print(f"{Fore.YELLOW} unauthorized")
            return
        elif json_message.get("files_exist"):
            print(f"{Fore.RED} file exist")
            return
        print(f"{Fore.GREEN} file uploaded")
    except FileNotFoundError:
        print(f" {Fore.RED} file with name {files.get('filename')} doesnt exist")


def list_files(args):
    if len(args) < 3:
        print('arguments missed')
        return
    files["username"] = args[1]
    files["password"] = args[2]
    socket.send(pickle.dumps(files))
    files_list = socket.recv_multipart()
    list_to_show = list(map(lambda filename: filename.decode("utf-8"), files_list))
    output = generate_output_files(list_to_show)
    print(f"{Fore.BLUE} {output} ")


def download(args):
    if len(args < 4):
        print('arguments missed')
        return
    filename = args[1]
    files["filename"] = filename.encode("utf-8")
    files["username"] = args[2]
    files["password"] = args[3]
    socket.send(pickle.dumps(files))
    download_info = socket.recv()
    json_info = pickle.loads(download_info)
    if json_info.get("fileNotFound"):
        print(f"{Fore.RED} the file does not exists {filename}")
        return
    with open(filename, "wb") as f:
        f.write(json_info.get("bytes"))
    print(f"{Fore.GREEN} {filename} downloaded")


# change name
def decide_commands():
    if len(sys.argv) <= 1:
        return "error"
    args = sys.argv[1:]
    command = args[0]
    password = getpass()
    args.append(password)

    files["command"] = command.encode("utf-8")
    if command == "upload":
        upload(args)

    elif command == "list":
        list_files(args)

    elif command == "download":
        download(args)
    elif command == "register":
        register(args)
    else:
        print("check command")
        return


def main():
    decide_commands()


if __name__ == "__main__":
    main()
