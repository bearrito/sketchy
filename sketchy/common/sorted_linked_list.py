import typing
from copy import  deepcopy

class CountingNode(object):

    def __str__(self):
        if self.item is not None:
            return "------>({me},{count})".format(me=self.item, count=self.count)
        else:
            return "ROOT"

    def __init__(self, item, back, forward=None, count:int = 0):
        self.item = item
        self.count = count
        self.forward = forward
        self.back = back

    def incr(self):
        self.count+=1

    def forward_link(self, node):
        self.forward = node

    def backward_link(self, node):
        self.back = node

    def swap_forward(self):
        cnt = deepcopy(self.count)
        item = deepcopy(self.item)
        self.item = self.forward.item
        self.count = self.forward.count
        self.forward.count = cnt
        self.forward.item = item

        return self.forward

class CountingLinkedList():

    def __str__(self):
        node = self.root
        stringy = ""
        while node.forward is not None:
            stringy += str(node)
            node = node.forward
        stringy += str(node)
        return stringy



    def __init__(self,skip_hint_size=0):
        self.root = CountingNode(None, None, None, -1)
        self.last = self.root
        self.index = {}

    def observe(self, item):
        if item in self.index:
            self._update(item, self.index[item])
        else:
            node = CountingNode(item, self.last, None, 1)
            self.index[item] = node
            self.last.forward_link(node)
            self.last = node

    def _update(self, item, node):
        node.incr()
        working_node = node
        while working_node.forward is not None and working_node.count > working_node.forward.count:
            working_node = working_node.swap_forward()
            self.index[working_node.back.item] = working_node.back
            self.index[working_node.item] = working_node

