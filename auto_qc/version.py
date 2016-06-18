def fetch_version():
    import os, pkg_resources
    path = os.path.join('..', 'VERSION')
    return pkg_resources.resource_string(__name__, path)

__version__ = fetch_version()
