if __name__ == '__main__':
    __package__ = 'listtools.listtypes'  # @ReservedAssignment
    import listtools  # @UnusedImport

from ..utilities import docs_from
from collections import MutableSet

__all__ = ['sortedlist', 'sortedset']

@docs_from(list)
class sortedlist(list):
    '''A list that preserves sorting. 
    
    Items can only be added or modified only if they preserve order. The special
    methods `.add()`, `update()` and `.modify()` modify the list putting items
    in the correct positions.
    
    The initial data will be sorted to be included in the list.
    '''
    def __init__(self, data, key=None, reverse=False):
        list.__init__(self, data)
        self.sort(key=key, reverse=reverse)

    @property
    def is_reversed(self):
        return self._reverse

    @property
    def key(self):
        return self._key

    def __repr__(self):
        data = list.__repr__(self)
        return '%s(%s)' % (type(self).__name__, data)

    #
    # Prevent modifications from altering the ordering of the list
    #
    def __setitem__(self, idx, value):
        # Checks if it preserves order with respect to the previous
        if idx and (not self._is_after(value, self[idx - 1])):
            raise ValueError('setting value to invalid order')

        # Checks if it preserves order with respect to the next
        if (idx < len(self) - 1) and (not self._is_after(self[idx + 1], value)):
            raise ValueError('setting value to invalid order')

        # Update to valid value
        list.__setitem__(self, idx, value)

    def insert(self, idx, value):
        # Checks if it preserves order with respect to the previous
        if idx and (self._cmp(value, self[idx - 1]) == -1):
            raise ValueError('setting value to invalid order')

        if self._cmp(self[idx], value) == -1:
            raise ValueError('setting value to invalid order')

        # Update to valid value
        list.insert(self, idx, value)

    def append(self, value):
        if self._cmp(value, self[-1]) == -1:
            raise ValueError('appending value to invalid order')
        list.append(self, value)

    def reverse(self):
        self._reverse = not self._reverse
        list.reverse(self)

    def sort(self, key=None, reverse=False):
        # Save comparison parameters
        self._reverse = reverse
        self._key = key

        # Define comparison function
        sign = (-1 if self._reverse else 1)
        if key is None:
            def cmp_func(x, y):
                return (1 if x > y else (-1 if x < y else 0)) * sign
        else:
            def cmp_func(x, y):
                x = key(x)
                y = key(y)
                return (1 if x > y else (-1 if x < y else 0)) * sign
        self._cmp = cmp_func

        # Sort items
        list.sort(self, key=key, reverse=reverse)

    def copy(self):
        L = list.copy(self)
        L._reverse = self._reverse
        L._key = self._key
        L._cmp = self._cmp

    def extend(self, L):
        sortedL = sorted(L, key=self.key, reverse=self._reverse)
        if L != sortedL:
            raise ValueError('extending with unordered data')
        if self._cmp(L[0], self[-1]) == -1:
            raise ValueError('extending to invalid order')
        list.extend(self, sortedL)

    def position(self, value):
        '''Return the index that a given value would have if it should belong 
        to the list.'''

        cmp = self._cmp
        sign = -1 if self._reverse else 1

        # Braket search for position that value would fit
        a, b = 0, len(self) - 1
        x, y = self[a], self[b]

        # Check if it is inside list
        if cmp(value, x) == -1:
            return 0
        if cmp(value, y) == 1:
            return len(self)

        # Reduce the braket at each iteration
        while a != b:
            c = a + ((b - a) // 2 or 1)
            z = self[c]
            if cmp(value, z) >= 0:
                a, x = c, z
            elif b != c:
                b, y = c, z
            else:
                break

        if cmp(value, x) == 1:
            return a + 1
        else:
            # Navegate the list searching for equal values
            N = len(self)
            while self[a] == x and a >= 0 and a < N:
                a -= sign
            return a + sign

    def index(self, value, *args):
        if args:
            return list.index(value, *args)
        try:
            idx = self.position(value)
        except ValueError:
            raise ValueError('%r is not in list' % value)
        if self[idx] == value:
            return idx
        else:
            raise ValueError('%r is not in list' % value)

    def add(self, value):
        '''Adds the given value to the list in the correct position.
        
        Return its index.'''

        idx = self.position(value)
        try:
            self.index(value)
        except IndexError:
            if idx == len(self):
                self.append(value)
            else:
                raise
            return idx

    def update(self, iterable):
        '''Add items in iterable in the correct postions.'''

        list.extend(self, iterable)
        self.sort(key=self._key, reverse=self._reverse)

    def modify(self, idx, obj):
        '''Remove the item at the given index and add `obj` to its correct 
        position on the list'''

        del self[idx]
        self.add(obj)

    def __add__(self, other):
        if isinstance(other, list):
            self.extend(other)
        else:
            raise TypeError

    def __mul__(self, n):
        return self +self * (n - 1)

@docs_from(set)
class sortedset(MutableSet):
    '''A sorted set.
    
    Items do not need to be hashable.'''

    def __init__(self, data, key=None, reverse=False):
        if isinstance(data, sortedlist):
            key = key or data.key
            reverse = reverse or data.reversed
        self._data = sortedlist(set(data), key=key, reverse=reverse)
        MutableSet.__init__(self)

    def __contains__(self, obj):
        try:
            self._data.index(obj)
            return True
        except ValueError:
            return False

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def add(self, obj):
        idx = self._data.position(obj)
        if self._data[idx] != obj:
            self._data.insert(idx, obj)

    def discard(self, obj):
        try:
            idx = self._data.index(obj)
        except ValueError:
            pass
        else:
            del self._data[idx]

    def __repr__(self):
        data = ', '.join(map(str, self._data))
        data = '[%s]' % data
        return '%s(%s)' % (type(self).__name__, data)


if __name__ == '__main__':
    L = [1, 2, 2, 2, 2, 2, 4, 8]
    s = sortedlist([1, 2, 3, 3, 3, 3, 4], reverse=False)
    s.add(10)
    print(s)

    s = sortedset([1, 2, 3, 3, 0])
    print(s)


    import doctest
    doctest.testmod()

    help(sortedlist)

