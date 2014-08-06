from os import path

def version():
    version_file = path.join(path.dirname(path.realpath(__file__)), '../../VERSION')
    with open(version_file, 'r') as f:
        return f.read().strip()

def major_version():
    return version().split('.')[0]
