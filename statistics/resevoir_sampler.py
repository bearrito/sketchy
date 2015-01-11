from random import randint, random, shuffle
import heapq
import math
from itertools import  repeat, cycle, chain


class ReservoirSampler(object):
    def __init__(self, size):
        self.size = size
        self.sample = []

    def observe(self, item):

        if len(self.sample) < self.size:
            self.sample[self.count] = item

        random_index = randint(0, self.count)
        if random_index < self.size:
            self.sample[random_index] = item

        self.count +=1

class WeightedReservoirSampler(object):
    def __init__(self, size, weights):
        self.weights = weights
        self.size = size
        self.sample = []

    def _compute_key(self, item):
        key = math.pow(random(), 1 / float(self.weights.get(item, 1)))
        return key


    def observe(self, item):

        if len(self.sample) < self.size:
            heapq.heappush(self.sample,(self._compute_key(item), item))
            self.count += 1
        else:
            key = self._compute_key(item)
            print("{item} and {key}".format(item=item,key=key))

            heapq.heappushpop(self.sample, (key, item))


