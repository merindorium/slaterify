class ExampleRequestText(object):
    pass


class PropertiesTable:
    HEADERS = ('Parameter', 'Type', 'Description')
    DATA_EXTRACT_SEQUENCE = ('name', 'property_type', 'description')


class Property:
    def __init__(self, property_type=None, description=None):
        self.property_type = property_type
        self.description = description or ''
        self.name = None


class SchemaObject:
    def __init__(self, object_type=None, properties=None, example=None):
        self.object_type = object_type
        self.properties = properties
        self.example = example

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


class Request:
    def __init__(self, request_body=None):
        self.request_body = request_body

        self.method = None
        self.route = None


class Path:
    HTTP_METHODS = ('get', 'post', 'put', 'delete')

    def __init__(self, summary=None, description=None, **requests):
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
    def __init__(self, info, paths):
        self.info = info
        self.paths = paths

        self._update_paths_route()

    def _update_paths_route(self):
        for route, path_node in self.paths.items():
            path_node.update_route(route)
