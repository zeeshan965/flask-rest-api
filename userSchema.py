from marshmallow import Schema, fields


class FormSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=lambda n: 18 <= n <= 100)
    gender = fields.Str(required=True, validate=lambda g: g in ['male', 'female'])
    phone = fields.Str(required=True)
    country = fields.Str(required=True)
