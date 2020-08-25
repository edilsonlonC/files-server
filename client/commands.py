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
    list_to_show = list(map(lambda filename: filename.decode("utf-8"), files_list))
    print(list_to_show)
