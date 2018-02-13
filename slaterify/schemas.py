from marshmallow import Schema, fields, pre_load

from node_schema import NodeSchema
from api_nodes import Document, Path, Request, RequestBody, Content, RequestContentType, SchemaObject, Property


class DocumentInfoSchema(Schema):
    title = fields.String()
    version = fields.String()
    description = fields.String()


class PropertySchema(NodeSchema):
    property_type = fields.String(load_from='type')
    description = fields.String()

    class Meta:
        model = Property


class PropertiesSchema(Schema):
    @pre_load
    def process_paths(self, data):
        for path in data.keys():
            self.declared_fields.update({
                path: fields.Nested(PropertySchema)
            })
            self.fields.update({
                path: fields.Nested(PropertySchema)
            })


class ObjectSchema(NodeSchema):
    object_type = fields.String(load_from='type')
    properties = fields.Nested(PropertiesSchema)
    example = fields.Dict()

    class Meta:
        model = SchemaObject


class RequestContentTypeSchema(NodeSchema):
    request_schema = fields.Nested(ObjectSchema, load_from='schema')

    class Meta:
        model = RequestContentType


class ContentSchema(NodeSchema):
    json_content = fields.Nested(RequestContentTypeSchema, load_from='application/json')

    class Meta:
        model = Content


class RequestBodySchema(NodeSchema):
    content = fields.Nested(ContentSchema)

    class Meta:
        model = RequestBody


class RequestSchema(NodeSchema):
    request_body = fields.Nested(RequestBodySchema, load_from='requestBody')

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
