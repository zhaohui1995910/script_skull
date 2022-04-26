# -*- coding: utf-8 -*-
# @Time    : 2021/9/28 17:58
# @Author  : 10867
# @FileName: fields.py
# @Software: PyCharm
from marshmallow import fields, ValidationError

# https://marshmallow.readthedocs.io/en/stable/custom_fields.html

from marshmallow import fields, ValidationError


class PinCode(fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return [int(c) for c in value]
        except ValueError as error:
            raise ValidationError("Pin codes must contain only digits.") from error
