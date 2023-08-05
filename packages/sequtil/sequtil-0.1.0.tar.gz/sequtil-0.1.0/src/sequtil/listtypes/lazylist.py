if __name__ == '__main__':
    __package__ = 'listtools.listtypes'  # @ReservedAssignment
    import listtools  # @UnusedImport

import itertools
from .base import Sequence
from ..utilities import docs_from

__all__ = ['lazylist']


@docs_from(list)
class lazylist(Sequence, list):

    '''A list whose members are calculated by consuming a (possibly infinite)
    iterator on-the-fly.

    Parameters
    ----------

    iterable : iterable object
        Any iterable object can be used to construct a list
    length : int
        The length can be specified if it is known beforehand. It can also be
        used to truncate the iterator at some given length. Infinite iterators
        can be explicitly specified by setting length='inf' or
        length=float('inf').

    Usage
    -----

    A lazy list only consumes its iterator when necessary. The consumed items
    can be found by printing the list. When it is just created, it have not
    consumed any elements from the iterator.

    >>> it = (x**2 for x in range(10))
    >>> L = lazylist(it); L
    lazylist([...])

    Asking for ``L[idx]`` forces the lazylist to consume a few elements from
    the iterator

    >>> L[3]
    9
    >>> L
    lazylist([0, 1, 4, 9, ...])

    Of course, we can consume a few items from the iterator and the lazylist
    will continue from this point

    >>> next(it), L[4]
    (16, 25)
    >>> L
    lazylist([0, 1, 4, 9, 25, ...])


    append()'s, extend()'s and, at to some extent pop()'s, can be done without
    consuming the iterator.

    >>> L.append('foo')
    >>> L.extend([1, 2]); L
    lazylist([0, 1, 4, 9, 25, ..., 'foo', 1, 2])

    Items can be `popped` from the `tail` of the lazylist without affecting the
    iterator

    >>> L.pop(), L.pop(), L.pop()
    (2, 1, 'foo')
    >>> L
    lazylist([0, 1, 4, 9, 25, ...])

    One more `pop()` forces the iterator to be consumed. This is completely
    transparent to the user

    >>> L.pop() # get the last item of iterator, i.e., 9**2
    81
    >>> L
    lazylist([0, 1, 4, 9, 25, 36, 49, 64])
    >>> L.is_iter_finished()
    True

    Infinite lists
    --------------

    There is nothing that prevents the lazylist from being infinite. User should
    set length argument to "inf" in order to prevent strange behavior.

    If length is not set, len(lazylist) will consume the whole iterator in
    order to calculate the correct length. This creates an infinite loop if
    the iterator never ends.

    >>> L = lazylist(range(10))
    >>> len(L); L
    10
    lazylist([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    This can be avoided by providing a length argument to the constructor. If
    length is shorter than the iterator, the later is truncated.

    >>> L = lazylist(range(10), 5)
    >>> len(L); L
    5
    lazylist([...])

    This works for infinite iterators as well. The argument of len() must be
    a positive integer. Since python does not have a infinite integer constant,
    an OverflowError is raised.

    >>> L = lazylist(itertools.count(), 'inf')
    >>> len(L)
    Traceback (most recent call last):
    ...
    OverflowError: cannot get the size of an infinite list

    All other operations that triggers the consumption of an infinite iterator
    raise an OverflowError.

    >>> L.pop()
    Traceback (most recent call last):
    ...
    OverflowError: cannot consume an infinite iterator
    '''

    _INF = float('inf')

    def __init__(self, iterable, length=None):
        list.__init__(self)
        self._iter = iter(iterable)
        self._tail = []
        self._iterlength = length
        if length == 'inf' or length == float('inf'):
            self._iterlength = self._INF

    def _consume(self):
        if self._iter is not None:
            if self._iterlength is self._INF:
                raise OverflowError('cannot consume an infinite iterator')
            list.extend(
                self,
                itertools.islice(
                    self._iter,
                    0,
                    self._iterlength))
            list.extend(self, self._tail)
            self._tail = []
            self._iter = None
            self._iterlength = 0

    def __getitem__(self, idx):
        if self._iterlength is not None:
            pre_length = self._iterlength + list.__len__(self)
            if idx >= pre_length:
                raise IndexError(idx)

        if idx < 0:
            try:
                return self._tail[idx]
            except IndexError:
                self._consume()
                return list.__getitem__(self, idx)

        else:
            for i, v in enumerate(self):
                if i == idx:
                    return v
            else:
                raise IndexError(idx)

    def __iter__(self):
        for v in list.__iter__(self):
            yield v

        if self._iter is not None:
            size = self._iterlength
            size = (size if size is not None else self._INF)
            for v in self._iter:
                if list.__len__(self) >= size:
                    self._consume()
                    return

                if size != self._INF:
                    size -= 1
                    self._iterlength = size
                list.append(self, v)
                yield v

        tail = self._tail
        self._consume()
        N = list.__len__(self)

        for i in range(N - len(tail), N):
            yield list.__getitem__(self, i)

    def __repr__(self):
        tname = type(self).__name__
        if self._iter is None:
            return '%s(%s)' % (tname, list.__repr__(self))
        else:
            pre_data = list.__repr__(self)[1:-1]
            pos_data = repr(self._tail)[1:-1]
            data = '...' if not pre_data else pre_data + ', ...'
            data = data if not pos_data else '%s, %s' % (data, pos_data)
            return '%s([%s])' % (tname, data)

    def append(self, value):
        if self._iter is None:
            list.append(self, value)
        else:
            self._tail.append(value)

    def extend(self, iterable):
        if self._iter is None:
            list.extend(self, iterable)
        else:
            self._tail.extend(iterable)

    def __len__(self):
        if self._iter is None:
            return list.__len__(self)
        elif self._iterlength == self._INF:
            raise OverflowError('cannot get the size of an infinite list')
        elif self._iterlength is not None:
            return list.__len__(self) + self._iterlength + len(self._tail)
        else:
            self._consume()
            return list.__len__(self)

    def __delitem__(self, idx):
        if idx < 0:
            try:
                del self._tail[idx]
                return
            except IndexError:
                pass

        self[idx]
        list.__delitem__(self, idx)

    def insert(self, idx, value):
        if idx < 0:
            try:
                self._tail[idx]
            except IndexError:
                pass
            else:
                self._tail.insert(idx, value)
                return

        self[idx]
        list.insert(self, idx, value)

    def is_iter_finished(self):
        '''Return True if the iterator was fully consumed'''

        return self._iter is None

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
