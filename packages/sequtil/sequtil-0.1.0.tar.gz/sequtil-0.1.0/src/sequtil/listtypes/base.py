if __name__ == '__main__':
    __package__ = 'listtools.listtypes'  # @ReservedAssignment
    import listtools  # @UnusedImport

import collections
from .. import api

__all__ = ['Sequence', 'immutable']

#===============================================================================
# Base sequence type
#===============================================================================
class Sequence(object):
    '''A Mapping base class that can be used to implement generic mappings
    by supplying the methods ``__getitem__``, ``__iter__``, ``__len__`` (for 
    immutable types), ``__delitem__``, and ``__setitem__`` (for mutable types).
    
    The implementation is borrowed from collections.MutableMapping and it is
    equivalent in most circumstances. ``Mapping`` however does not use abstract
    classes. This allows arbitrary meta-classes being used for the derived types.
    '''
    def __init__(self):
        if type(self) is Sequence:
            raise TypeError("'Mapping' should be instanced by child classes")

    def __delitem__(self, key):
        msg = "'%s' instance does not support deletion" % type(self).__name__
        raise ValueError(msg)

    def __getitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        raise NotImplementedError

    def __setitem__(self, key, value):
        msg = "'%s' instance does not support mutation" % type(self).__name__
        raise ValueError(msg)

    def insert(self, idx, value):
        msg = "'%s' instance does not support mutation" % type(self).__name__
        raise ValueError(msg)

    def __repr__(self):
        try:
            name = type(self).__name__
            data = ', '.join(map(repr, self))
            return '%s([%s])' % (name, data)
        except NotImplementedError:
            return object.__repr__(self)

    __eq__ = api.isequal.generic  # @UndefinedVariable
    sort = api.sort.generic  # @UndefinedVariable

for name in dir(collections.MutableSequence):
    if (name.startswith('_') and not name.startswith('__')
            or name in ('__module__', '__metaclass__')):
        continue
    if not hasattr(Sequence, name):
        method = getattr(collections.MutableSequence, name)
        if callable(method):
            try:
                setattr(Sequence, name, method.im_func)
            except AttributeError:
                setattr(Sequence, name, method)
del name, method

#===============================================================================
# Immutable sequences
#===============================================================================
class immutable(Sequence):
    '''Creates an immutable (and hashable) view of a sequence object.
    
    The hash is computed the first time the hash(obj) is executed. It is the
    responsability of the user to *do not* modify data while the `immutable`
    lives in order to keep this hash value consistent.
    
    Examples
    --------
    
    >>> l1 = immutable([1, 2])
    >>> l1[0] = 1
    ...
    ValueError: 'immutable' instance does not support mutation
    '''

    def __init__(self, data):
        self._data = data
        self.__hash = None

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getattr__(self, attr):
        return getattr(self._data, attr)

    def __hash__(self):
        try:
            return self.__hash
        except AttributeError:
            try:
                self.__hash = hash(self._data)
            except TypeError:
                self.__hash = hash(tuple(self._data))
            return self.__hash

    @property
    def data(self):
        return self._data

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

