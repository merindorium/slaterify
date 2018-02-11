from marshmallow import post_load
from marshmallow.schema import BaseSchema, SchemaOpts, with_metaclass, SchemaMeta


class NodeSchemaOpts(SchemaOpts):
    def __init__(self, meta):
        super(NodeSchemaOpts, self).__init__(meta)
        self.model = getattr(meta, 'model', None)


class NodeSchema(with_metaclass(SchemaMeta, BaseSchema)):
    OPTIONS_CLASS = NodeSchemaOpts

    @post_load
    def make_instance(self, data):
        return self.opts.model(**data)
