"""
The `list` module defines data structures that support ordered and linked storage 
of elements.
"""
from typing import Generic, Iterable, Iterator, Optional, TypeVar
from collections import OrderedDict

T = TypeVar("T")
K = TypeVar("K")


class LinkedOrderedDictNode(Generic[T]):
    """
    A node in the linked list used by the `LinkedOrderedDict`.
    """

    def __init__(self, val: T):
        self.val = val
        self.prev: Optional["LinkedOrderedDictNode[T]"] = None


class LinkedOrderedDict(Generic[K, T], Iterable[T]):
    """
    A custom ordered dictionary that maintains the insertion order of keys while
    linking each node to the previous one.
    """

    def __init__(self):
        self._list: OrderedDict[K, LinkedOrderedDictNode[T]] = OrderedDict()

    def head(self) -> Optional[LinkedOrderedDictNode[T]]:
        """
        Returns the most recently inserted node without removing it.
        """
        # Reinsert to get peek O(1) effect
        if self._list:
            (node_key, node) = self._list.popitem()
            self._list[node_key] = node
            return node

    def get(self, key: K) -> Optional[LinkedOrderedDictNode[T]]:
        return self.__getitem__(key)

    def __setitem__(self, key: K, val: T):
        node = LinkedOrderedDictNode(val)
        node.prev = self.head()
        self._list[key] = node

    def __getitem__(self, key: K) -> Optional[LinkedOrderedDictNode[T]]:
        return self._list.get(key)

    def __contains__(self, key: K) -> bool:
        return key in self._list

    def __iter__(self) -> Iterator[T]:
        for node in self._list.values():
            yield node.value

    def __delitem__(self, key: K):
        if key in self._list:
            del self._list[key]
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return len(self._list)
