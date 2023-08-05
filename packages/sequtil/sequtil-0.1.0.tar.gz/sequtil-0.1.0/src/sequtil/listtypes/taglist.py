if __name__ == '__main__':
    __package__ = 'listtools.listtypes'  # @ReservedAssignment
    import listtools  # @UnusedImport

from .base import Sequence


class Node(object):

    '''Base node object that is used internally in tagged lists'''

    def __init__(self, data, tag=None):
        self.data = data
        self.tag = tag

    def __iter__(self):
        yield self.data
        yield self.tag

    def __len__(self):
        return 2


class Tags(Sequence):

    def __init__(self, owner):
        self._owner = owner
        self._data = owner._data

    def __getitem__(self, i):
        return self._data[i].tag

    def __setitem__(self, i, value):
        self._data[i].tag = value

    def __iter__(self):
        return (t for (x, t) in self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        name = type(self).__name__.lower()
        data = ', '.join(map(repr, self))
        return '%s([%s])' % (name, data)


class taglist(Sequence):
    __slots__ = ['tags', '_data']

    def __init__(self, data=[]):
        '''A list-like object whose items can be tagged

        Usage
        -----

        >>> L = taglist([1, 2, 3, 4])
        >>> L.tags[0] = 'one'
        >>> L
        taglist([1, 2, 3, 4])
        >>> L.tags
        tags(['one', None, None, None])
        '''
        self._data = [Node(x) for x in data]
        self.tags = Tags(self)

    def __getitem__(self, idx):
        return self._data[idx].data

    def __len__(self):
        return len(self._data)

    def __delitem__(self, idx):
        del self._data[idx]

    def __setitem__(self, idx, value):
        self._data[idx] = Node(value)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, [x.data for x in self._data])

    def insert(self, idx, value):
        self._data.insert(idx, Node(value))

    # Interaction with tag information ########################################
    def items(self):
        """L.items() --- returns an iterator over all (obj, tag) pairs."""

        for x in self._data:
            yield x.data, x.tag

    def popitem(self, index=-1):
        """L.pop_item([index]) ==> (object, tag)

        Remove and return a tuple with object and tag at index (default last)
        """

        return list.pop(self, index)

    def filter_by_tag(self, tag=None, key=None, filter_out=False):
        """L.filter_by_tag(function)

        Filter items by tag value."""

        if key is None:
            if filter_out:
                self._data = [x for x in self._data if x.tag != tag]
            else:
                self._data = [x for x in self._data if x.tag == tag]
        else:
            if filter_out:
                self._data = [x for x in self._data if not key(x.tag)]
            else:
                self._data = [x for x in self._data if key(x.tag)]

    def sort_by_tag(self, key=None, reverse=False):
        """L.sort(cmp=None, key=None, reverse=False) -- stable sort by tag
        value *IN PLACE*"""

        if key is None:
            keyfunc = lambda x: x.tag
        else:
            keyfunc = lambda x: key(x.tag)

        self._data.sort(key=keyfunc, reverse=reverse)

    def sort_by_item(self, key, reverse=False):
        """L.sort(cmp=None, key=None, reverse=False) -- stable sort *IN PLACE*
        cmp(x, y) -> -1, 0, 1

        Apply the cmp(x,y) function to the tuples of (object, tag)"""

        keyfunc = lambda x: key(x.tag, x.value)

        self._data.sort(key=keyfunc, reverse=reverse)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
