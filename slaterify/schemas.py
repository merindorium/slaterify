from marshmallow import Schema, fields, pre_load

from node_schema import NodeSchema
from api_nodes import Document, Path, Request


class DocumentInfoSchema(Schema):
    title = fields.String()
    version = fields.String()
    description = fields.String()


class RequestSchema(NodeSchema):
    request_body = fields.Dict(load_from='requestBody')
    responses = fields.Dict()

    class Meta:
        model = Request


class ApiEndpoint(NodeSchema):
    summary = fields.String()
    description = fields.String()
    get = fields.Nested(RequestSchema)
    post = fields.Nested(RequestSchema)

    class Meta:
        model = Path


class DocumentPaths(Schema):
    @pre_load
    def process_paths(self, data):
        for path in data.keys():
            self.declared_fields.update({
                path: fields.Nested(ApiEndpoint)
            })
            self.fields.update({
                path: fields.Nested(ApiEndpoint)
            })


class DocumentSchema(NodeSchema):
    info = fields.Nested(DocumentInfoSchema)
    paths = fields.Nested(DocumentPaths)

    class Meta:
        model = Document
