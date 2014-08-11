from fn import iters as it

def is_variable(var):
    """
    Is the string a variable reference?
    """
    return isinstance(var, basestring) and it.head(var) == ':'

def split_into_namespace_and_path(variable_string):
    drop_colon = variable_string[1:]
    path_array = drop_colon.split('/')
    return [it.head(path_array), it.tail(path_array)]

def get_analysis(analyses, var):
    namespace, _ = split_into_namespace_and_path(var)
    return it.head(filter(lambda x: x['analysis'] == namespace, analyses))

def get_variable_value(analysis, var):
    _, path = split_into_namespace_and_path(var)
    return reduce(lambda a, k: a[k], path, analysis['outputs'])

def variable(analyses, path):
    analysis = get_analysis(analyses, path)
    return get_variable_value(analysis, path)
