# coding=utf-8
import time

#
# def timeit(fn):
#     def warp(*args, **kwargs):
#         start = time.clock()
#         fn(*args, **kwargs)
#         end = time.clock()
#
#         print 'used:', end - start
#     return warp
import timeit

l1 = ['abs', 'bdd', 'cadas', 'dfdfdc', 'cc']
l2 = [u'abs', u'bdd', u'cadas', u'dfdfdc', u'cc']


def f1():
    'cc' in l1


def f2():
    u'cc' in l1


def f3():
    'cc' in l2


def f4():
    u'cc' in l2


# f1()
# f2()
# f3()
# f4()

# f4 ~= f1 < f2 ~= f3
# 差不多三倍的时间 由于编码转换
if __name__ == '__main__':
    _r = 5
    _n = 1000000
    # print(timeit.repeat("f1()", setup="from __main__ import f1", repeat=_r, number=_n))
    # print(timeit.repeat("f2()", setup="from __main__ import f2", repeat=_r, number=_n))
    # print(timeit.repeat("f3()", setup="from __main__ import f3", repeat=_r, number=_n))
    # print(timeit.repeat("f4()", setup="from __main__ import f4", repeat=_r, number=_n))
    a = 'asd'
    b= unicode(a)
    print b

# 我写代码的时候,发现  unocode, str 的比较操作耗时特别长
# 我想看一下
# ```
#     if u'a' in ['a','b','c']:
#         pass
# ```
# 这个`in` 操作的具体执行流程,但是在pycharm里打了断点,直接跳过去了
# 请问怎么在pycharm里debug到C语言的层级呢,或者用其他什么工具可以?


# in COMPARE_OP