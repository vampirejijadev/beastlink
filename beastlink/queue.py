import random


class Queue:
    def __init__(self):
        self._items = []

    async def add(self, track):
        self._items.append(track)

    async def get(self):
        if self._items:
            return self._items.pop(0)
        return None

    async def clear(self):
        self._items.clear()

    def peek(self):
        if self._items:
            return self._items[0]
        return None

    def remove(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def shuffle(self):
        random.shuffle(self._items)

    def all(self):
        return list(self._items)

    def size(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0