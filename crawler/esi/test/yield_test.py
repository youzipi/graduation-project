def a():
    for i in xrange(10):
        yield 10
        yield i

b = a()

for i in b:
    print(i)