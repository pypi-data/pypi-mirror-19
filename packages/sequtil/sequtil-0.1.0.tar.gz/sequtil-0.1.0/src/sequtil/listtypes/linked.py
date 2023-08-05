from listtools.utilities import docs_from
from collections import MutableSequence


class NodeError(ValueError):
    pass


class sNode(object):

    '''Represents a node element in a single linked list'''

    __slots__ = ['_next', 'data']

    def __init__(self, next, data):
        self._next = next
        self.data = data

    def __repr__(self):
        return '%s(..., %s)' % (type(self).__name__, self.data)

    next = property(lambda x: x._next)

    def iter_forward(self):
        '''Iterates through the linked nodes in the forward direction'''

        yield self
        node = self
        while node._next:
            yield node
            node = node._next

    def data_forward(self):
        '''Iterates through the data stored in the linked nodes in the forward
        direction'''

        yield self.data
        node = self
        while node._next:
            yield node.data
            node = node._next

    def jump(self, i=1, raises=False):
        '''Return the node i positions ahead.

        Return None of the node does not exists. If raises is True, a
        NodeError is raised.'''

        node = self
        try:
            for _ in range(i):
                node = node._next
        except AttributeError:
            node = None

        if raises and node is None:
            raise NodeError('node does not exists')
        return node

    def last(self):
        '''Return the last node of the chain'''

        node = self
        while node._next:
            node = node._next
        return node


class dNode(sNode):

    '''Represents a node element in a double linked list'''

    __slots__ = ['_prev', '_next', 'data']

    def __init__(self, prev, next, data):
        self._prev = prev
        self._next = next
        self.data = data

    prev = property(lambda x: x._prev)

    def iter_backwards(self):
        '''Iterates through the linked nodes in the backwards direction'''

        yield self
        node = self
        while node._prev:
            yield node
            node = node._prev

    def data_backwards(self):
        '''Iterates through the data stored in the linked nodes in the backwards
        direction'''

        yield self.data
        node = self
        while node._prev:
            yield node.data
            node = node._prev

    def jump(self, i=1, raises=False):
        '''Return the node i positions ahead. Negative indexes are accepted
        in order to travel backwards.

        Return None of the node does not exists. If raises is True, a
        NodeError is raised.
        '''
        node = self
        try:
            if i >= 0:
                for _ in range(i):
                    node = node._next
            else:
                for _ in range(-i):
                    node = node._prev
        except AttributeError:
            node = None

        if raises and node is None:
            raise NodeError('node does not exists')
        return node

    def first(self):
        '''Return the first node of the chain'''

        node = self
        while node._prev:
            node = node._prev
        return node


###############################################################################
#                         Linked lists
###############################################################################


@docs_from(list)
class dlinkedlist(MutableSequence):

    '''
    Double linked list.

    Insertions and deletions are fast if happens in the both extremes of the
    list. All operations in the middle of the list are slow, including item
    access, which is O(n).

    Exposes a list interface to the user. The user also have access to the
    internal implementation as a list of linked nodes. The `first_node` and
    `last_node` attributes points to the corresponding nodes. The attribute
    `size` caches the list size.

    Examples
    --------

    A dlinkedlist can be used as a regular list for the most part

    >>> L = dlinkedlist([1, 2, 3, 4, 5])

    Appends and insertions work as expected

    >>> L.append(6)
    >>> L.insert(0, 0); L
    dlinkedlist([0, 1, 2, 3, 4, 5, 6])

    The same as pops and deletions

    >>> L.pop()
    6
    >>> del L[0]; L
    dlinkedlist([1, 2, 3, 4, 5])


    Or loops and item access

    >>> L[2]
    3
    >>> for x in L:
    ...     print(x)
    1
    2
    3
    4
    5

    Besides the list operations, we can access the underlying node structure

    >>> node = L.get_node(2)

    Nodes have a next, prev and data attributes

    >>> node.next, node.data
    (dNode(..., 4), 3)

    We can also walk through the node tree using some auxiliary methods

    >>> node.jump(-2)
    dNode(..., 1)

    >>> list(node.iter_forward())
    [dNode(..., 3), dNode(..., 3), dNode(..., 4)]
    '''
    __slots__ = ['_first', '_last', '_size']

    def __init__(self, data):
        self._size = 0
        for x in data:
            self.append(x)

    def __repr__(self):
        tname = type(self).__name__
        return '%s(%s)' % (tname, list(self))

    def __iter__(self):
        try:
            link = self._first
            while link is not None:
                yield link.data
                link = link._next
        except AttributeError:
            return

    def append(self, value):
        try:
            new = dNode(self._last, None, value)
            self._last._next = new
            self._last = new
        except AttributeError:
            try:
                new = self._first._next = dNode(self._first, None, value)
                self._last = new
            except AttributeError:
                self._first = dNode(None, None, value)
        self._size += 1

    # Abstract methods ########################################################
    def __delitem__(self, idx):
        if idx < 0:
            idx = self._size + idx
        if not idx:
            if self._size >= 2:
                self._first = self._first._next
                self._first._prev = None
        elif idx == self._size - 1:
            self._last = self._last._prev
            self._last._next = None
        else:
            link = self.get_node(idx)
            link._prev._next = link._next
            link._next._prev = link._prev
        self._size -= 1
        if self._size <= 1:
            del self._last
            if self._size == 0:
                del self._first

    def __getitem__(self, idx):
        return self.get_node(idx).data

    def __len__(self):
        return self._size

    def __setitem__(self, idx, value):
        self.get_node(idx).data = value

    def insert(self, idx, value):
        if idx < 0:
            idx = self._size + idx
        if idx == self._size:
            self.append(value)
        elif not idx:
            self._first = dNode(None, self._first, value)
            self._size += 1
        else:
            link = self.get_node(idx)
            new = dNode(link._prev, link, value)
            link._prev._next = new
            link._prev = new
            self._size += 1

    # Utility methods and special methods for double linked lists #############
    def swap(self, i, j):
        '''Swap the values in i and j'''

        link1 = self.get_node(min(i, j))
        link2 = link1
        for _ in range(abs(i - j)):
            link2 = link2._next
        link1.data, link2.data = link2.data, link1.data

    def bogosort(self):
        '''Implements the bogosort algorithm inplace. This is usually less
        efficient than the regular `sort()` but can be faster if the list is
        almost ordered except from a few swapped entries.
        '''

        if self._size <= 1:
            return

        swaps = 1
        prev = None
        while swaps:
            swaps = 0
            curr = self._first
            next_ = curr._next
            while next_:
                if curr.data > next_.data:
                    next_.data, curr.data = curr.data, next_.data
                    if prev is not None and curr.data < prev.data:
                        swaps += 1
                prev = curr
                curr = next_
                next_ = next_._next

    def get_node(self, idx):
        '''Returns the link at index idx'''

        if idx < 0:
            idx = self._size + idx
        try:
            if idx < (self._size / 2):
                return self._first.jump(idx, True)
            else:
                return self._last.jump(idx - self._size + 1, True)
        except NodeError:
            raise IndexError(idx)
        except AttributeError:
            if self._size == 0:
                raise IndexError(idx)
            raise

    # Properties ##############################################################
    @property
    def first_node(self):
        return self._first

    @property
    def last_node(self):
        return self._last

    @property
    def first(self):
        return self._first.data

    @first.setter
    def first(self, value):
        self._first.data = value

    @property
    def last(self):
        return self._last.data

    @last.setter
    def last(self, value):
        self._last.data = value


@docs_from(list)
class linkedlist(MutableSequence):

    '''Single linked lists.

    Slightly faster and more memory efficient than double liked lists, but
    offer fast access only to the beginning of the list.

    Examples
    --------

    A linkedlist can be used as a regular list for the most part

    >>> L = linkedlist([1, 2, 3, 4, 5])

    Appends and insertions work as expected

    >>> L.append(6)
    >>> L.insert(0, 0); L
    linkedlist([0, 1, 2, 3, 4, 5, 6])

    The same as pops and deletions

    >>> L.pop()
    6
    >>> del L[0]; L
    linkedlist([1, 2, 3, 4, 5])


    Or loops and item access

    >>> L[2]
    3
    >>> for x in L:
    ...     print(x)
    1
    2
    3
    4
    5

    Besides the list operations, we can access the underlying node structure

    >>> node = L.get_node(2)

    Nodes have a next and data attributes

    >>> node.next, node.data
    (sNode(..., 4), 3)

    We can also walk through the node tree using some auxiliary methods

    >>> node.jump(2)
    sNode(..., 5)

    >>> list(node.iter_forward())
    [sNode(..., 3), sNode(..., 3), sNode(..., 4)]
    '''

    __slots__ = ['_first', '_size']

    # Use some implementations from dlinkedlist
    __init__ = dlinkedlist.__init__
    __getitem__ = dlinkedlist.__getitem__
    __init__ = dlinkedlist.__init__
    __iter__ = dlinkedlist.__iter__
    __len__ = dlinkedlist.__len__
    __setitem__ = dlinkedlist.__setitem__
    __repr__ = dlinkedlist.__repr__
    bogosort = dlinkedlist.bogosort
    swap = dlinkedlist.swap
    first = dlinkedlist.first
    first_node = dlinkedlist.first_node

    def get_node(self, idx):
        '''Returns the link at index idx'''

        if idx < 0:
            idx = self._size + idx
        try:
            return self._first.jump(idx, True)
        except NodeError:
            raise IndexError(idx)
        except AttributeError:
            if self._size == 0:
                raise IndexError(idx)
            raise

    def append(self, value):
        new = sNode(None, value)
        try:
            self.get_node(self._size - 1)._next = new
        except IndexError:
            self._first = new
        self._size += 1

    def insert(self, idx, value):
        if idx < 0:
            idx = self._size + idx
        if idx == self._size:
            self.append(value)
        elif idx == 0:
            self._first = sNode(self._first, value)
            self._size += 1
        else:
            link = self.get_node(idx - 1)
            new = sNode(link._next, value)
            link._next = new
            self._size += 1

    def __delitem__(self, idx):
        if idx < 0:
            idx = self._size + idx
        if idx == 0:
            if self._size:
                self._first = self._first.next
            else:
                del self._first
        else:
            link = self.get_node(idx - 1)
            link._next = link._next._next
            self._size -= 1
            if self._size == 0:
                del self._first

if __name__ == '__main__':
    import doctest
    doctest.testmod()
