from functools import partial


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def typed_property(name, expected_type):
    storage_name = '_' + name

    @property
    def propp(self):
        return getattr(self, storage_name)

    @propp.setter
    def propp(self, value):
        if not isinstance(value, expected_type):
            raise TypeError('{0} must be a {1},found {2}'.format(name, expected_type, type(value)))
        setattr(self, storage_name, value)

    return propp


String = partial(typed_property, expected_type=str)
Integer = partial(typed_property, expected_type=int)


class User(object):
    name = String('name')
    age = Integer('age')

    def __init__(self):
        pass

    def __str__(self):
        return str(self.__dict__)


a = User()
a.age = 12
a.name = '11'
print a
