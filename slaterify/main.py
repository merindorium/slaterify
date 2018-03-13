import json
import sys

from jinja2 import Environment, PackageLoader

from slaterify.schemas import DocumentSchema


def main():
    file_path = sys.argv[1]

    env = Environment(loader=PackageLoader('slaterify', 'templates'))
    template = env.get_template('document.md.jinja2')

    with open(file_path, 'r') as api:
        data = json.load(api)
        document, _ = DocumentSchema(strict=True).load(data)

    rendered_data = template.render(document=document)

    with open('../rendered_api.md', 'w') as rf:
        rf.write(rendered_data)


if __name__ == '__main__':
    main()
