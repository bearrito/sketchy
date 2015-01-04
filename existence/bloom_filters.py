import typing
import hashlib
from array import array
from itertools import repeat
from collections import Iterable
import sys

from abc import ABCMeta, abstractmethod


class ExistenceChecker:
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, observable):
        pass

    @abstractmethod
    def exists(self, observable) -> bool:
        pass


class BloomFilter(ExistenceChecker):
    def __init__(self, size, num_hashes):
        assert (size > 0 and num_hashes > 0)
        self.num_hashes = num_hashes
        self.size = size
        self.filter = array('i', repeat(0, self.size))

    def _internal_hash(self, key, i:int) -> int:
        sha = hashlib.sha384()
        sha.update(str(i).encode('utf-8'))
        sha.update(key.encode('utf-8'))
        hash = int(sha.hexdigest(), 16) % self.size
        return hash

    def _hashes(self, key):

        hashes = [self._internal_hash(key, i + 1) for i in range(self.num_hashes)]
        return hashes

    def _insert_at(self, idx : int):
        self.filter[idx] = 1

    def insert(self, observable):
        [self._insert_at(idx) for idx in self._hashes(observable)]

    def exists(self, observable) -> bool:
        for idx in self._hashes(observable):
            entry = self.filter[idx]
            if entry == 0:
                return False
        return True


class CountingBloomFilter(BloomFilter):

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


counting_bloom = CountingBloomFilter(1000, 32)
counting_bloom.insert("ss")
e0 = counting_bloom.exists("ss")
c0 = counting_bloom.count("ss")
counting_bloom.insert("ss")
c0 = counting_bloom.count("ss")

counting_bloom.delete("ss")
e1 = counting_bloom.exists("ss")
c1 = counting_bloom.count("ss")
a = 1