from slaterify.utils import add_component, get_component


class ExampleRequestText(object):
    pass


class PropertiesTable:
    HEADERS = ('Parameter', 'Type', 'Description')
    DATA_EXTRACT_SEQUENCE = ('name', 'property_type', 'description')


class Property:
    def __init__(self, property_type=None, description=''):
        self.property_type = property_type
        self.description = description or ''
        self.name = None


class SchemaObject:
    def __init__(self, object_type=None, properties=None, example=None, ref=None):
        self.object_type = object_type
        self.properties = properties
        self.example = example
        self.ref = ref

    def update(self):
        if self.ref:
            component = get_component(self.ref)
            self.properties = component.properties
            self.example = component.example
            self.object_type = component.object_type

        if self.properties:
            self._update_properties()

    def _update_properties(self):
        for property_name, property_node in self.properties.items():
            property_node.name = property_name


class RequestContentType:
    def __init__(self, request_schema):
        self.request_schema = request_schema


class Content:
    def __init__(self, json_content):
        self.json_content = json_content


class RequestBody:
    def __init__(self, content):
        self.content = content

    @property
    def schema(self):
        schema = self.content.json_content.request_schema
        schema.update()
        return schema


class Request:
    def __init__(self, request_body=None):
        self.request_body = request_body

        self.method = None
        self.route = None


class Path:
    HTTP_METHODS = ('get', 'post', 'put', 'delete')

    def __init__(self, summary='', description='', **requests):
        self.summary = summary
        self.description = description
        self.requests = requests

        self.route = None

    def update_route(self, route):
        self.route = route
        self._update_methods()

    def _update_methods(self):
        for method in self.HTTP_METHODS:
            request = self.requests.get(method)

            if request:
                request.method = method
                request.route = self.route


class Document:
    COMPONENTS_PATH_BASE = '#/components/{}/{}'

    def __init__(self, info, paths, components):
        self.info = info
        self.paths = paths
        self.components = components

        self._update_paths_route()
        self._register_components()

    def _update_paths_route(self):
        for route, path_node in self.paths.items():
            path_node.update_route(route)

    def _register_components(self):
        for components_type, components in self.components.items():
            for component_name, component in components.items():
                component_path = self.COMPONENTS_PATH_BASE.format(components_type, component_name)
                add_component(component_path, component)
