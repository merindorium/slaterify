import nodes
import json


class Annotation(nodes.Text):
    def render(self):
        return f'> {self.text}'


class ExampleRequestText(nodes.Text):
    def render(self):
        blocks = list()
        request_body = json.dumps(self.text, indent=4)

        blocks.append(Annotation('Example Request').render())
        blocks.append(nodes.MultiCode(request_body, syntax='json').render())

        return '\n\n'.join(blocks)


class PropertiesTable(nodes.Table):
    HEADERS = ('Parameter', 'Type', 'Description')
    DATA_EXTRACT_SEQUENCE = ('name', 'property_type', 'description')


class Property:
    def __init__(self, property_type, description=None):
        self.property_type = property_type
        self.description = description or ''
        self.name = None


class SchemaObject(nodes.Node):
    def __init__(self, object_type, properties, example=None):
        self.object_type = object_type
        self.properties = properties
        self.example = example

        self._update_properties()

    def render(self):
        blocks = list()

        blocks.append(PropertiesTable(self.properties.values()).render())

        return '\n\n'.join(blocks)

    def _update_properties(self):
        for property_name, property_node in self.properties.items():
            property_node.name = property_name


class RequestContentType(nodes.Node):
    def __init__(self, request_schema):
        self.request_schema = request_schema

    def render(self):
        blocks = list()

        blocks.append(ExampleRequestText(self.request_schema.example).render())
        blocks.append(nodes.H3('Attributes').render())
        blocks.append(self.request_schema.render())

        return '\n\n'.join(blocks)


class Content(nodes.Node):
    def __init__(self, json_content):
        self.json_content = json_content

    def render(self):
        return self.json_content.render()


class RequestBody(nodes.Node):
    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content.render()


class Request(nodes.Node):
    def __init__(self, request_body=None):
        self.request_body = request_body

        self.method = None
        self.route = None

    def render(self):
        blocks = list()

        blocks.append(nodes.H3('HTTP Request').render())
        blocks.append(nodes.Code(f'{self.method.upper()} {self.route}').render())

        if self.request_body:
            blocks.append(self.request_body.render())

        return '\n\n'.join(blocks)


class Path(nodes.Node):
    HTTP_METHODS = ('get', 'post', 'put', 'delete')

    def __init__(self, summary, description, **requests):
        self.summary = summary
        self.description = description
        self.__dict__.update(**requests)

        self.route = None

    def render(self):
        blocks = list()

        blocks.append(nodes.H1(self.summary).render())
        blocks.append(nodes.Text(self.description).render())

        for method in self.HTTP_METHODS:
            request = getattr(self, method, None)

            if request:
                blocks.append(request.render())

        return '\n\n'.join(blocks)

    def update_route(self, route):
        self.route = route
        self._update_methods()

    def _update_methods(self):
        for method in self.HTTP_METHODS:
            request = getattr(self, method, None)

            if request:
                request.method = method
                request.route = self.route


class Document(nodes.Node):
    def __init__(self, info, paths):
        self.info = info
        self.paths = paths

        self._update_paths_route()

    def render(self):
        blocks = []

        for path in self.paths.values():
            blocks.append(path.render())

        return '\n\n'.join(blocks)

    def _update_paths_route(self):
        for route, path_node in self.paths.items():
            path_node.update_route(route)
