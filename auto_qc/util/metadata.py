from os import path

def get_version():
    version_file = path.join(path.dirname(path.realpath(__file__)), '../../VERSION')
    with open(version_file, 'r') as f:
        return f.read().strip()
