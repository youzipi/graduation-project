_len = len
def test(l):
    print _len(l)
    for i in xrange(_len(l)):
        print l[i]




for i in xrange(100000):
    test('2345sdad')
