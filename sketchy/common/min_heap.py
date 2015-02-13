from itertools import count
from heapq import heappush,heappop

class MinHeap(object):
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = '<removed-task>'
        self.counter = count()

    def add_item(self, item, priority=0):

        cnt= 1
        if item in self.entry_finder:
            cnt = self.remove_item(item) + 1
        entry = [priority, cnt, item]
        self.entry_finder[item] = entry
        heappush(self.pq, entry)

    def remove_item(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED
        return entry[1]

    def pop_item(self):
        while self.pq:
            priority, cnt, item = heappop(self.pq)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def peak(self):
        return self.pq[0]