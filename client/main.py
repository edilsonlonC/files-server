#!/home/edilson/anaconda3/bin/python3.8

import zmq
import sys
import sys
import pickle
from utilities import generate_output_files
from colorama import Fore


files = {}

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def upload(args):
    files["filename"] = args[1].encode("utf-8")
    try:
        file = open(files.get("filename"), "rb")
        if "/" in args[1]:
            files["filename"] = args[1].split("/")[-1].encode("utf-8")
            print(files.get("filename"))

        bytes_file = file.read()
        files["bytes"] = bytes_file
        socket.send(pickle.dumps(files))
        message = socket.recv_string()
        print(f"{Fore.GREEN} {message}")
    except FileNotFoundError:
        print(f" {Fore.RED} file with name {files.get('filename')} doesnt exist")


def list_files(args):
    socket.send(pickle.dumps(files))
    files_list = socket.recv_multipart()
    list_to_show = list(map(lambda filename: filename.decode("utf-8"), files_list))
    output = generate_output_files(list_to_show)
    print(f"{Fore.BLUE} {output} ")


def download(args):
    filename = args[1]
    files["filename"] = filename.encode("utf-8")
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
def decide_commads():
    if len(sys.argv) <= 1:
        return "error"
    args = sys.argv[1:]
    command = args[0]

    files["command"] = command.encode("utf-8")
    if command == "upload":
        upload(args)

    elif command == "list":
        list_files(args)

    elif command == "download":
        download(args)
    else:
        print("check command")
        return


def main():
    decide_commads()


if __name__ == "__main__":
    main()
