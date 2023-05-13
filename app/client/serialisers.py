import marshmallow_sqlalchemy as ma
from marshmallow import pre_load, post_dump, fields

from app.client.models import Client


class ClientSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Client

    id = fields.Str(dump_only=True)
    name = fields.Str()

    @pre_load
    def make_client(self, data, **kwargs):  # noqa
        return data

    @post_dump
    def dump_client(self, data, **kwargs):  # noqa
        return data
