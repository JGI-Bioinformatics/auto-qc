def failed(status):
    failing = map(lambda n: n['node']['fail'], status['node_results'])
    return any(failing)

def version():
    import os
    path = os.path.join(os.path.dirname(__file__), '../VERSION')
    with open(path, 'r') as f:
        return f.read().strip()

def simple(status):
    return 'FAIL' if failed(status) else 'PASS'

def yaml(status):
    import yaml
    output = {
        'fail'      : failed(status),
        'metadata'  : {'version': {'auto-qc': version()}},
        'thresholds': status['node_results']
    }
    return yaml.dump(output, default_flow_style=False).strip()
