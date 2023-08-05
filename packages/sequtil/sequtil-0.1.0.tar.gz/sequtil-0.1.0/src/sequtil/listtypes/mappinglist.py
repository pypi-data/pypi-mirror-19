if __name__ == '__main__':
    __package__ = 'listtools.listtypes'  # @ReservedAssignment
    import listtools  # @UnusedImport

from .base import Sequence

class mappinglist(Sequence):
    '''A list that works as a transformmed view of some sequence data. The user 
    must define a transformation function and optionally can set the inverse
    transformation in order to allow for writing back in the original list.
    
    Usage
    -----
    
    >>> L0 = [1, 2, 3, 4]
    >>> L1 = mappinglist(L0, lambda x: x**2); L1
    [1, 4, 9, 16]
    
    '''

    NO_INV_FUNC_ERROR = ValueError('Cannot set values if invfunc is not set')

    def __init__(self, raw, func, invfunc=None):
        self.raw = raw
        self.func = func
        self.invfunc = invfunc

    def __repr__(self):
        func = self.func
        tname = type(self).__name__
        return repr([ func(x) for x in self.raw ])

    #===========================================================================
    # Basic Sequence API
    #===========================================================================
    def __getitem__(self, idx):
        return self.func(self.raw[idx])

    def __len__(self):
        return len(self.raw)

    def __delitem__(self, idx):
        del self.raw[idx]

    def __setitem__(self, idx, value):
        if self.invfunc is None:
            raise self.NO_INV_FUNC_ERROR
        else:
            raw_value = self.invfunc(value)
            self.raw[idx] = raw_value

    def insert(self, idx, value):
        if self.invfunc is None:
            raise self.NO_INV_FUNC_ERROR
        else:
            raw_value = self.invfunc(value)
            self.raw.insert(idx, raw_value)

    #===========================================================================
    # Additional list methods
    #===========================================================================
    def reverse(self):
        self.raw.reverse()

    def sort(self, key=None, reverse=False):
        data = zip(self, self.raw)
        if key is not None:
            key, oldkey = lambda x: oldkey(x[0])
        data = sorted(data, key=key, reverse=reverse)
        self.raw[:] = [ x[1] for x in data ]

    #===========================================================================
    # Specific mapping list methods
    #===========================================================================
    def items(self):
        '''Iterates over all (raw, transformed) values pairs'''

        func = self.func
        for x in self.raw:
            yield (x, func(x))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
