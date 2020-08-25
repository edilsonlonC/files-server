import zmq
import sys
import sys
import pickle

files = {}

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")



def upload(args):
    files["filename"] = args[1].encode("utf-8")
    try:
        file = open(files.get("filename"), "rb")
        bytes_file = file.read()
        files["bytes"] = bytes_file
        socket.send(pickle.dumps(files))
        message = socket.recv()
        print(message)
    except FileNotFoundError:
        print(f"file with name {files.get('filename')} doesnt exist")


def list_files(args):
    socket.send(pickle.dumps(files))
    files_list = socket.recv_multipart()
    list_to_show= list(map(lambda filename: filename.decode('utf-8'),files_list))
    print(list_to_show)


def download (args):
    filename = args[1]
    files["filename"] = filename.encode("utf-8")
    socket.send(pickle.dumps(files))
    bytes_to_save = socket.recv()
    if bytes_to_save == b'error in server':
        return 'error'
    with open(filename,"wb") as f:
        f.write(bytes_to_save)

 


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


def main():
    decide_commads()


if __name__ == "__main__":
    main()
