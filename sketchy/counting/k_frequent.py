from array import array
from itertools import  repeat
from sketchy.common.min_heap import MinHeap




class KFrequent(object):

    def __init__(self, num_registers : int):
        self.num_registers = num_registers
        self.buckets = array('l', repeat(0, self.num_registers))
        self.item_index = {}

        self.min_heap = MinHeap()

        self.observed_count = 0
        self.is_initialized = False

    def observe(self, item):
        """
        :param item: Any hashable object
        :return: Observe the hashable object meaning increment or add the object to the counting index
        """

        if item in self.item_index:
            item_index = self.item_index[item]
            self.buckets[item_index] += 1
            self.min_heap.add_item(item, self.buckets[item_index])
        else:

            if self.is_initialized:
                min_item = self.min_heap.pop_item()
                bucket_index = self.item_index[min_item]
                del self.item_index[min_item]
                self.item_index[item] = bucket_index
                self.buckets[bucket_index] += 1
                self.min_heap.add_item(item, bucket_index + 1)
            else:

                self.min_heap.add_item(item, 1)
                self.item_index[item] = self.observed_count
                self.buckets[self.observed_count] = 1

                self.observed_count +=1
                if self.observed_count == self.num_registers:
                    self.is_initialized = True

    def most_frequent_with_counts(self):
        """
        :return: Returns a dictionary of at most K keys.
        The value of each key will be the approximate number of times that key has been observed
        """
        result = {}
        for (key, value) in self.item_index.items():
            result[key] = self.buckets[value]
        return result







