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
    socket.send(info_to_send)
    response = socket.recv()
    json_response = pickle.loads(response)
    if not json_response.get("user_saved"):
        username = info_user.get("username")
        print(f"username {username} exists")
        return
    print("user created")


def register(args):
    if len(args) < 2:
        print("arguments are missing")
        return
    password = getpass()
    if not password:
        print('you need a password')
        exit(1)
    files["username"] = args[1]
    files["password"] = password
    send_register(files)


def upload(args):
    if len(args) < 3:
        print("arguments missed")
        return
    password = getpass()
    if not password:
        exit(1)
    files["filename"] = args[1].encode("utf-8")
    files["username"] = args[2]
    files["password"] = password
    try:
        file = open(files.get("filename"), "rb")
        if "/" in args[1]:
            files["filename"] = args[1].split("/")[-1].encode("utf-8")

        bytes_file = file.read()
        files["bytes"] = bytes_file
        socket.send(pickle.dumps(files))
        response = socket.recv()
        json_message = pickle.loads(response)
        if json_message.get("unauthorized"):
            print(f"{Fore.YELLOW} unauthorized")
            return
        elif json_message.get("newname"):
            newname = json_message.get("newname")
            print(
                f"{Fore.LIGHTRED_EX} The file exists. if you want to add it as a {newname} press c, if you want to overwrite r and e to exit"
            )
            option = input()
            if option == "c":
                json_message["filename"] = newname.encode("utf-8")
                socket.send(pickle.dumps(json_message))
                response = socket.recv()
            elif option == "r":
                json_message["rewrite"] = True
                json_message["filename"] = (json_message.get("filename")).encode(
                    "utf-8"
                )
                socket.send(pickle.dumps(json_message))
                response = socket.recv()
            else:
                exit(0)
            return
        print(f"{Fore.GREEN} file uploaded")
    except FileNotFoundError:
        print(f" {Fore.RED} file with name {files.get('filename')} does not exist")


def list_files(args):
    if len(args) < 2:
        print("arguments are missing")
        return
    password = getpass()
    if not password:
        exit(1)
    files["username"] = args[1]
    files["password"] = password
    socket.send(pickle.dumps(files))
    files_list = socket.recv_multipart()
    list_to_show = list(map(lambda filename: filename.decode("utf-8"), files_list))
    output = generate_output_files(list_to_show)
    print(f"{Fore.LIGHTYELLOW_EX} {output} ")


def download(args):
    if len(args) < 3:
        print("arguments are missing")
        return
    password = getpass()
    filename = args[1]
    files["filename"] = filename.encode("utf-8")
    files["username"] = args[2]
    files["password"] = password
    if not password:
        exit(1)
    socket.send(pickle.dumps(files))
    download_info = socket.recv()
    json_info = pickle.loads(download_info)
    if json_info.get("unauthorized"):
            print(f"{Fore.YELLOW} unauthorized")
            return
    if json_info.get("fileNotFound"):
        print(f"{Fore.RED} the file does not exists {filename}")
        return
    with open(filename, "wb") as f:
        f.write(json_info.get("bytes"))
    print(f"{Fore.GREEN} {filename} downloaded")


# change name
def decide_commands():
    if len(sys.argv) <= 1:
        print("arguments are missing")
        return
    args = sys.argv[1:]
    command = args[0]
  

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
