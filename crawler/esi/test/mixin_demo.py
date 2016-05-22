class Mixin1(object):
    a = 1

    def __init__(self):
        print("Mixin1")


class Mixin2(object):
    a = 2

    def __init__(self):
        print("Mixin2")


class Class1(Mixin1, Mixin2):

    def __init__(self):
        super(Class1, self).__init__()
        Mixin2.__init__(self)

        print("Test init")
        print("a=", str(self.a))


a = Class1()
