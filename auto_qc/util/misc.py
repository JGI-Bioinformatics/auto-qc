def virtual_env(project_root):
    from os.path import join
    activate = join(project_root,'vendor', 'python', 'bin', 'activate_this.py')
    execfile(activate, dict(__file__ = activate))
