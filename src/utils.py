def get_content(file):
    # Read file content
    file = open(file, "r")
    s = file.read()
    file.close()
    return s
