# Copyright (c) 2017 Luiz Menezes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

from .exceptions import EmptyField, ValidationError


class Model:
    fields = ()
    allow_empty = ()

    def __init__(self, **kwargs):
        for field_name in self.fields:
            field_value = kwargs.get(field_name, None)
            setattr(self, field_name, field_value)

    def is_empty(self, value):
        return bool(value)

    def validate(self, raise_exception=True):
        for field_name in self.fields:
            value = getattr(self, field_name)

            allow_empty = field_name in self.allow_empty
            if not allow_empty and not self.is_empty(value):
                if raise_exception:
                    raise EmptyField(field_name)
                return False

            try:
                validate_field = getattr(self, 'validate_{}'.format(field_name))
            except AttributeError:
                continue

            try:
                validate_field(value)
            except ValidationError:
                if raise_exception:
                    raise
                return False

        return True

    def serialize(self):
        self.validate()
        return {field_name: getattr(self, field_name) for field_name in self.fields}
