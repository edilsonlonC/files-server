from database import get_files_same_name


def get_filename(idfile, filename):
    extension = filename.split(".")[-1]
    return f"{idfile}.{extension}"


def get_possible_name(filename):
    
    name, ext = filename.split(".")
    print(name)
    same_names_in_db = get_files_same_name(name)
    same_names = list(map(lambda filedb: filedb[1] , same_names_in_db))
    print(same_names)
    print(type(same_names))
    for sm in range(len(same_names)):
        new_name = f"{name}({sm+1}).{ext}"
        if not new_name in same_names:
            return new_name
