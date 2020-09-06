from database import get_files_same_name


def get_filename(idfile, filename):
    extension = filename.split(".")[-1]
    return f"{idfile}.{extension}"


def get_possible_name(filename, id_user):

    name, ext = filename.rsplit(".", 1)
    same_names_in_db = get_files_same_name(name, id_user)
    same_names = list(map(lambda filedb: filedb[1], same_names_in_db))

    for sm in range(len(same_names)):
        new_name = f"{name}({sm+1}).{ext}"
        if not new_name in same_names:
            return new_name
