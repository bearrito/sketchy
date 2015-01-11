
import hashlib
from array import array
from bitarray import bitarray
from itertools import repeat
import sys
import pickle
import math

from abc import ABCMeta, abstractmethod


class ExistenceChecker:
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, observable):
        pass

    @abstractmethod
    def exists(self, observable) -> bool:
        pass
    @abstractmethod
    def merge(self, filter):
        pass

    @abstractmethod
    def error_rate(self) -> float:
        pass



    def _internal_hash(self, key, i:int) -> int:
        sha = hashlib.sha384()
        sha.update(str(i).encode('utf-8'))
        sha.update(key.encode('utf-8'))
        hash = int(sha.hexdigest(), 16) % self.size
        return hash

    def _hashes(self, key):
        hashes = [self._internal_hash(key, i + 1) for i in range(self.num_hashes)]
        return hashes



class BloomFilterMerge(object):
    def __init__(self, size:int, num_hashes:int, filter):
        self.size = size
        self.num_hashes = num_hashes
        self.filter = filter

class BloomFilter(ExistenceChecker):
    def __init__(self, size, num_hashes):
        assert (size > 0 and num_hashes > 0)
        self.num_hashes = num_hashes
        self.size = size
        self.filter = bitarray(self.size)
        self._count = 0



    def _insert_at(self, idx : int):
        self.filter[idx] = 1

    def insert(self, observable):
        self._count +=1
        [self._insert_at(idx) for idx in self._hashes(observable)]

    def exists(self, observable) -> bool:
        for idx in self._hashes(observable):
            entry = self.filter[idx]
            if entry == 0:
                return False
        return True

    def merge_view(self):
        return pickle.dumps(BloomFilterMerge(self.size,self.num_hashes, self.filter ))

    def error_rate(self) -> float:
       return math.pow(1 - math.exp(-self.num_hashes * self._count / float(self.size)), self.num_hashes)

    def merge(self, bloom_filter_merge):
        mergeable = pickle.loads(bloom_filter_merge)

        preconditions = [
            mergeable.size == self.size,
            mergeable.num_hashes == self.num_hashes
        ]

        if all(preconditions):
            for idx,location,  in enumerate(mergeable.filter):
                self.filter[idx] = (self.filter[idx] or location)





class CountingBloomFilter(BloomFilter):

    def __init__(self, size, num_hashes):
        assert (size > 0 and num_hashes > 0)
        self.num_hashes = num_hashes
        self.size = size
        self.filter = array('i',repeat(0,self.size))


    def _insert_at(self, idx : int):
        self.filter[idx] += 1

    def _internal_delete(self, observable):
        for idx in self._hashes(observable):
            self.filter[idx] -= 1

    def delete(self, observable):
        if self.exists(observable):
            self._internal_delete(observable)

    def count(self, observable) -> int:
        current_min = sys.maxsize
        for idx in self._hashes(observable):
            entry = self.filter[idx]
            current_min = min(current_min,entry)
        return  current_min


