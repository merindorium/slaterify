_components = {}


def add_component(path, data):
    _components[path] = data


def get_component(path):
    try:
        return _components[path]
    except KeyError:
        raise NameError('There is no component with path {}'.format(path))
