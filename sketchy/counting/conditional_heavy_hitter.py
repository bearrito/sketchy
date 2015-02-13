import typing
from sketchy.common.hash_provider import HashProvider
from sketchy.common.min_heap import MinHeap


class ConditionalParentChild(HashProvider):
    def __init__(self):
        self.heap = MinHeap()

    def observe(self, child):
        self.heap.add_item(child)

    def least_frequent_child(self)-> (object, int):

        top = self.heap.peak()
        return (top[2],top[1])
        

class ConditionalHeavyHitter(HashProvider):

    def __init__(self, hash_group_size:int):
        self.hash_group_size = hash_group_size
        self.parent_child_index = {}
        self.parents = {}
        self.hash_group_frequencies = {}


    def observe(self,parent, child):
        heap = self.parents[parent]





