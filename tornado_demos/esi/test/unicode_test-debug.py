"""Small snippet to raise an IndexError."""


def test():
    a = ['a', 'b', 'c']
    w = u'a'
    if w in a:
        print 1

''
if __name__ == '__main__':
    test()
