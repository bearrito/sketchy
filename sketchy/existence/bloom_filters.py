from array import array
from itertools import repeat
import sys
import math

import hashlib
from bitarray import bitarray
from abc import ABCMeta, abstractmethod

from sketchy.protocols.messages_pb2 import BloomMerge


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
        hash = int(sha.hexdigest(), 16) % self.width
        return hash

    def _hashes(self, key):
        hashes = [self._internal_hash(key, i + 1) for i in range(self.depth)]
        return hashes


class BloomFilter(ExistenceChecker):
    def __init__(self, width, depth):
        assert (width > 0 and depth > 0)
        self.depth = depth
        self.width = width
        self.filter = bitarray(self.width)
        self.filter.setall(False)
        self._count = 0

    def _insert_at(self, idx : int):
        self.filter[idx] = True

    def insert(self, observable):
        self._count += 1
        for idx in self._hashes(observable):
            self._insert_at(idx)

    def exists(self, observable) -> bool:
        for idx in self._hashes(observable):
            entry = self.filter[idx]
            if entry == 0:
                return False
        return True

    def merge_view(self):

        update = BloomMerge()

        update.width = self.width
        update.depth = self.depth
        for idx, key in enumerate(self.filter):
            if key:
                update.ones_indices.append(idx)

        return update

    def error_rate(self) -> float:
       return math.pow(1 - math.exp(-self.depth * self._count / float(self.width)), self.depth)

    def merge(self, update):


        preconditions = [
            update.width == self.width,
            update.depth == self.depth
        ]

        if all(preconditions):
            for location in update.ones_indices:
                self.filter[location] = True





class CountingBloomFilter(ExistenceChecker):

    def __init__(self, width, depth):
        assert (width > 0 and depth > 0)
        self.depth = depth
        self.width = width
        self.filter = array('i',repeat(0, self.width))

    def insert(self, observable):
        for idx in self._hashes(observable):
            self._insert_at(idx)

    def _insert_at(self, idx : int):
        self.filter[idx] += 1

    def _internal_delete(self, observable):
        for idx in self._hashes(observable):
            self.filter[idx] -= 1

    def delete(self, observable):
        if self.exists(observable):
            self._internal_delete(observable)

    def count(self, observable) -> int:
        current_min = sys.maxwidth
        for idx in self._hashes(observable):
            entry = self.filter[idx]
            current_min = min(current_min,entry)
        return current_min

    def exists(self, observable) -> bool:
        for idx in self._hashes(observable):
            entry = self.filter[idx]
            if entry == 0:
                return False
        return True


