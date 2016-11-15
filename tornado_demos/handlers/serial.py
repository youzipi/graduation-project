from bson.json_util import dumps


class A(object):
    pass


class B(object):
    def __init__(self):
        self.b = 12
        self.c = '123'


a = A()
a.b = [1, 2, 3]

a.c = "12"
a.d = B()

print(dumps(a))
