from threading import Thread, Event
from functools import wraps

import time

import timeout_decorator


class MyThread(Thread):
    def __init__(self, function, interval=1):
        """

        :param event:
        :param timeout:
        :return:
        """
        Thread.__init__(self)
        if not callable(function):
            raise AssertionError("'{0}' is not an function!!".format(str(function)))
        else:
            self.func = function
        self.interval = interval
        self.stopped = Event()

    def run(self):
        while not self.stopped.wait(self.interval):
            self.func()

    def stop(self):
        self.stopped.set()



def atom():
    print('atom')

thread = MyThread(function=atom, interval=5)
thread.start()

# a = 'abc'
# thread = MyThread(a)
# thread.start()

time.sleep(13)
thread.stop()
# stopFlag = Event()
# thread = MyThread(stopFlag)
# thread.start()
#
# time.sleep(5)
# stopFlag.set()


# def print_name(ss):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             print func.__name__
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator
def print_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print func.__name__
        return func(*args, **kwargs)

    return wrapper

#
# def timeout(cycle):
#     def decorate(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             while not self.stopped.wait(self.timeout):
#             return func(*args, **kwargs)
#
#         return wrapper
#     return decorate


@print_name
# @timeout(100)
@timeout_decorator.timeout(20)
def timeout_test():
    print("start")
    for i in range(10):
        time.sleep(1)
        print(i)

# timeout_test()
# print 111
