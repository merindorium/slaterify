class Node:
    def render(self):
        raise NotImplementedError


class Text(Node):
    def __init__(self, text):
        self.text = text

    def render(self):
        return self.text


class H1(Text):
    def render(self):
        return '# {}'.format(self.text)


class H2(Text):
    def render(self):
        return '## {}'.format(self.text)


class H3(Text):
    def render(self):
        return '### {}'.format(self.text)


class H4(Text):
    def render(self):
        return '#### {}'.format(self.text)


class Code(Text):
    def render(self):
        return '`{}`'.format(self.text)


class MultiCode(Text):
    def render(self):
        return '```\n{}\n```'.format(self.text)


class Request(Node):
    def __init__(self, responses, request_body=None):
        self.request_body = request_body
        self.responses = responses

        self.method = None
        self.route = None

    def render(self):
        blocks = list()

        blocks.append(H3('HTTP Request').render())
        blocks.append(Code('{} {}'.format(self.method.upper(), self.route)).render())

        return '\n\n'.join(blocks)


class Path(Node):
    HTTP_METHODS = ('get', 'post', 'put', 'delete')

    def __init__(self, summary, description, **requests):
        self.summary = summary
        self.description = description
        self.__dict__.update(**requests)

        self.route = None

    def render(self):
        blocks = list()

        blocks.append(H1(self.summary).render())
        blocks.append(Text(self.description).render())

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


class Document(Node):
    def __init__(self, info, paths):
        self.info = info
        self.paths = paths

        self._update_paths_route()

    def render(self):
        data = []

        for path in self.paths.values():
            data.append(path.render())

        return data

    def _update_paths_route(self):
        for route, path_node in self.paths.items():
            path_node.update_route(route)
