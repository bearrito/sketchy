import asyncio
import typing

class PeriodicTask(object):
    def __init__(self, mergeable):
        self.mergeable = mergeable

    @asyncio.coroutine
    def broadcast(self):
        self.mergeable.build_merge_object()



