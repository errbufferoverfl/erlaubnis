from marshmallow import fields, Schema, pre_load, post_dump

from app.user.models import User


class UserSchema(Schema):
    class Meta:
        model = User

    username = fields.Str()
    password = fields.Str(load_only=True)
    last_login_at = fields.Str(dump_only=True)
    current_login_at = fields.Str(dump_only=True)
    last_login_ip = fields.Str(dump_only=True)
    current_login_ip = fields.Str(dump_only=True)

    @pre_load
    def make_user(self, data, **kwargs):  # noqa
        return data

    @post_dump
    def dump_user(self, data, **kwargs):  # noqa
        return {"user": data}


class UserSessionSchema(Schema):
    username = fields.Str()
    password = fields.Str(load_only=True)


user_schema = UserSchema()
user_session_schema = UserSessionSchema()
