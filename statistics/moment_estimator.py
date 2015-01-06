from math import pow
from random import random,shuffle
from itertools import chain, repeat


def identity(arg):
    return arg

def second_moment(arg):
    return pow(arg,2)

class AMSEstimator(object):
    def __init__(self,  function=second_moment):
        self.function = function
        self._count = 0
        self._current_item = None
        self._image = 0

    def _bernoulli_trial(self):
        threshold = 1 / float(self._count)
        if random() < threshold:
            return True
        else:
            return False

    def observe(self, item):
        self._count +=1
        if self._bernoulli_trial():
            self._current_item = item
            self._image = 1
        else:
            if item == self._current_item:
                self._image +=1


    def estimate(self):
        a =  self.function(self._image)
        b =  self.function(self._image - 1)
        return self._count * (a - b)



a = list(chain(*chain(repeat([1, 2,], 100),repeat([3, 4], 1000))))
shuffle(a)
b = 1