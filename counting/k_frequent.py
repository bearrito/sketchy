from array import array
from itertools import  repeat
from sys import  maxsize
from itertools import count
from heapq import heappush,heappop


class MinHeap(object):
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = '<removed-task>'
        self.counter = count()

    def add_item(self, item, priority=0):

        if item in self.entry_finder:
            self.remove_item(item)
        cnt = next(self.counter)
        entry = [priority, cnt, item]
        self.entry_finder[item] = entry
        heappush(self.pq, entry)

    def remove_item(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED

    def pop_item(self):
        while self.pq:
            priority, cnt, item = heappop(self.pq)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')


class KFrequent(object):

    def __init__(self, num_registers : int):
        self.num_registers = num_registers
        self.buckets = array('l', repeat(0, self.num_registers))
        self.item_index = {}

        self.min_heap = MinHeap()

        self.observed_count = 0
        self.is_initialized = False


    def observe(self, item):

        if item in self.item_index:
            item_index = self.item_index[item]
            current_count = self.buckets[item_index]

            self.buckets[item_index] = current_count + 1
            self.min_heap.add_item(item, current_count + 1)
        else:

            if self.is_initialized:

                min_item = self.min_heap.pop_item()
                bucket_index = self.item_index[min_item]
                del self.item_index[min_item]
                self.item_index[item] = bucket_index
                self.buckets[bucket_index] =  self.buckets[bucket_index] + 1
                self.min_heap.add_item(item, bucket_index + 1)

            else:


                self.min_heap.add_item(item, 1)
                self.item_index[item] = self.observed_count
                self.buckets[self.observed_count] = 1

                self.observed_count +=1
                if self.observed_count == self.num_registers:
                    self.is_initialized = True

    def most_frequent_with_counts(self):
        result = {}
        for (key, value) in self.item_index.items():
            result[key] = self.buckets[value]
        return result







