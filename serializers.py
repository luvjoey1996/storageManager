from marshmallow import Schema, fields, validate

from config import Configuration
from models import ServiceType


class CreateServiceSchema(Schema):
    type = fields.Str()


class ServiceCreateSchema(Schema):
    type = fields.Int(validate=validate.OneOf(choices=ServiceType.as_choices()))
    memory = fields.Int(validate=validate.Range(min=1, max=Configuration.MEMORY_TOTAL - Configuration.MEMORY_RESERVE),
                        missing=1)


class PaginationSchema(Schema):
    page_size = fields.Int(validate=validate.Range(min=10, max=30))
    current_page = fields.Int(validate=validate.Range(min=1))


class ServicePagingSchema(Schema):
    name = fields.Str()
    type = fields.Int()


class SettingSchema(Schema):
    type = fields.Int()
    name = fields.Str()
    value = fields.Str()


class ServiceSchema(Schema):
    name = fields.Str()
    type = fields.Int()
    memory = fields.Int()
    state = fields.Int()
    error_no = fields.Int()
    settings = SettingSchema(many=True)

    username = fields.Str()
    password = fields.Str()
    port = fields.Int()
    ip = fields.Str()
