from abc import ABCMeta, abstractproperty
import hashlib

class HashProvider:
    __metaclass__ = ABCMeta

    @abstractproperty
    def depth(self):
        return -1

    @abstractproperty
    def width(self):
        return -1

    def _internal_hash(self, key, i:int) -> int:
        sha = hashlib.sha384()
        sha.update(str(i).encode('utf-8'))
        sha.update(key.encode('utf-8'))
        hash = int(sha.hexdigest(), 16) % self.width
        return hash

    def _hashes(self, item):
        hashes = [self._internal_hash(item, i + 1) for i in range(self.depth)]
        return hashes