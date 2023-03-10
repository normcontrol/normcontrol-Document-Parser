"""
    A file with methods for loading the document correctly.
"""

def create_path(abs_path, rel_path):
    script_dir = str.split(abs_path, '/')
    path = ''
    ind = 0
    while ind < len(script_dir) - 2:
        path += script_dir[ind]
        path += '/'
        ind += 1
    return path + rel_path