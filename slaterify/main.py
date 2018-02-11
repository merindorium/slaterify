import json
import sys

from schemas import DocumentSchema

if __name__ == '__main__':
    file_path = sys.argv[1]

    with open(file_path, 'r') as api:
        data = json.load(api)
        document, _ = DocumentSchema(strict=True).load(data)

    rendered_data = document.render()

    with open('rendered_api.md', 'w') as rf:
        rf.write(rendered_data)
