import zmq
import pickle
import json
import os


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def uplodad_file(filename, bytes_to_save):
    with open(f"files/{filename}", "wb") as f:
        f.write(bytes_to_save)


def list_files():
    files_list = os.listdir("files")
    print(type(files_list))
    list_to_send = list(map(lambda filename: filename.encode("utf-8"), files_list))
    socket.send_multipart(list_to_send)


def download(filename):
    try:
        file = open(f"files/{filename}", "rb")
        bytes_to_download = file.read()
        socket.send(bytes_to_download)
    except FileNotFoundError:
        print("error")
        socket.send(b"error in server")


def commands(files):
    command = files.get("command")
    if command == b"upload":
        filename = files.get("filename").decode("utf-8")
        bytes_to_save = files.get("bytes")
        uplodad_file(filename, bytes_to_save)
        socket.send_string("prueba")
    elif command == b"list":
        list_files()
    elif command == b"download":
        filename = files.get("filename").decode("utf-8")
        download(filename)


def main():
    while True:
        print("server is running")
        message = socket.recv()
        files = pickle.loads(message)
        commands(files)


if __name__ == "__main__":

    main()
