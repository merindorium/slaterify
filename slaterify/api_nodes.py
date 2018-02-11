import nodes


class Request(nodes.Node):
    def __init__(self, responses, request_body=None):
        self.request_body = request_body
        self.responses = responses

        self.method = None
        self.route = None

    def render(self):
        blocks = list()

        blocks.append(nodes.H3('HTTP Request').render())
        blocks.append(nodes.Code('{} {}'.format(self.method.upper(), self.route)).render())

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
