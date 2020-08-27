def get_filename(idfile, filename):
    extension = filename.split(".")[-1]
    return f"{idfile}.{extension}"
