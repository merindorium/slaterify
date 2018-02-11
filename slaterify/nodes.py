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
