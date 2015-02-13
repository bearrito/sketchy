import array
import sys

from sketchy.common.hash_provider import HashProvider


class CountMinSketch(HashProvider):
    def __init__(self, width:int, depth:int):
        self._width = width
        self._depth = depth
        self.sketch = {}
        self._initialize_sketch()

    @property
    def width(self):
        return self._width
    @property
    def depth(self):
        return self._depth

    def _initialize_sketch(self):
        for idx in range(self.depth):
            self.sketch[idx] = array.array('l', range(0, self.width))

    def observe(self, item):
        for idx, hash in enumerate(self._hashes(item)):
            self.sketch[idx][hash] += 1

    def count(self,item):
        current_min = sys.maxsize
        for idx, hash in enumerate(self._hashes(item)):
            current_min = min(self.sketch[idx][hash], current_min)
        return current_min
