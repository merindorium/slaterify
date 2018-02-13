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
        return f'# {self.text}'


class H2(Text):
    def render(self):
        return f'## {self.text}'


class H3(Text):
    def render(self):
        return f'### {self.text}'


class H4(Text):
    def render(self):
        return f'#### {self.text}'


class Code(Text):
    def render(self):
        return f'`{self.text}`'


class MultiCode(Text):
    def __init__(self, text, syntax=None):
        super(MultiCode, self).__init__(text)
        self.syntax = syntax or ''

    def render(self):
        return f'```{self.syntax}\n{self.text}\n```'


class TableRow(Text):
    ROW_PATTERN = '{} |'

    def render(self):
        return self.ROW_PATTERN.format(self.text)


class Table(Node):
    HEADERS = ()
    DATA_EXTRACT_SEQUENCE = ()

    def __init__(self, data):
        self.data = data

    def render(self):
        blocks = list()

        blocks.append(self.render_header())
        blocks.append(self.render_data())

        return '\n'.join(blocks)

    def render_header(self):
        text_row = ''
        border_row = ''

        for column in self.HEADERS:
            border_width = '-' * len(column)

            border = TableRow(border_width).render()
            header = TableRow(column).render()

            text_row += header
            border_row += border

        return f'{text_row}\n{border_row}'

    def render_data(self):
        data_rows = []
        for item in self.data:
            item_row = ''

            for column in self.DATA_EXTRACT_SEQUENCE:
                column_data = getattr(item, column)
                item_row += TableRow(column_data).render()

            data_rows.append(item_row)

        return '\n'.join(data_rows)
