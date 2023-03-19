"""
    A file with methods for loading the document correctly.
"""
import platform

def create_path(abs_path, rel_path):
    cur_platform = platform.platform()
    if "macOS" in cur_platform:
        script_dir = str.split(abs_path, '/')
    else:
        script_dir = str.split(abs_path, '\\')
    path = ''
    ind = 0
    while ind < len(script_dir) - 2:
        path += script_dir[ind]
        path += '/'
        ind += 1
    return path + rel_path