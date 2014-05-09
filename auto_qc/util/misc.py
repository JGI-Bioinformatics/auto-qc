def virtual_env(project_root):
    from os.path import join
    activate = join(project_root,'env','bin','activate_this.py')
    execfile(activate, dict(__file__ = activate))
