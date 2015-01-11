import typing
import math

class LossyCountTriple(object):
    def __init__(self, item, estimated_frequency:float, max_error:float):
        self.item = item
        self.estimated_frequency = estimated_frequency
        self.max_error = max_error

    def increment(self):
        self.estimated_frequency += 1

    def can_purge(self,threshold):
        return (self.estimated_frequency + self.max_error <= threshold)


class LossyCounter(object):
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.width = math.ceil(1 / math.floor(epsilon))
        self._n = 0
        self._bucket_generation = 1
        self._triples = {}

    def purge(self):
        if self._n % self.width:
            purgeable = []

            #Need to check if I can delete while enumerating
            for k, triple in self._triples.values():
                if triple.can_purge():
                    purgeable.append(k)
            for p in purgeable:
                del self._triples[p]

    def observe(self, item):
        self._n +=1
        if item in self.triples:
            self._triples[item].increment()
        else:
            self._triples[item] = LossyCountTriple(item, 1, self._bucket_generation - 1,)

    def freqeunt(self, support):
        threshold = (support - self.epsilon) * self._n

        result = []
        for triple in self._triples:
            if triple.estimated_frequency >= threshold:
                result.append(triple)

        return result



