class Mixin1(object):
    def __init__(self):
        print("Mixin1")


class Mixin2(object):
    def __init__(self):
        print("Mixin2")


class Class1(Mixin1, Mixin2):
    def __init__(self):
        super(Class1, self).__init__()
        Mixin2.__init__(self)

        print("Test init")


a = Class1()
