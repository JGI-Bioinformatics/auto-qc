from fn import iters as it

def is_variable(var):
    """
    Is the string a variable reference?
    """
    return isinstance(var, basestring) and it.head(var) == ':'

def is_variable_path_valid(analysis, path):
    """
    Does the variable path have a matching value in the analysis?
    """
    try:
        get_variable_value(analysis, path)
    except KeyError as e:
        return False
    return True

def get_variable_value(analysis, path):
    """
    Get variable value by traversing path into analysis
    """
    drop_colon = path[1:]
    path_array = drop_colon.split('/')
    return reduce(lambda a, k: a[k], path_array, analysis['data'])
