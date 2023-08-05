'''

List API functions
------------------

These include all the magic functions (such as __getitem__, __setitem__, etc) and
the API (append, insert, etc). So it is equivalent to use

>>> [1, 2, 3][0] == getitem([1, 2, 3], 0)
True

By default, all these generic API functions try to execute the object's own
implementation. So `contains(L, 0)` simply executes `L.__contains__(0)`. Only 
when `L` does have a `__contains__` method, the generic implementation is executed.

One can force the execution of this generic implementations by using the `.generic`
attribute of these functions. e.g., `contains.generic(L, 0)` will execute the 
generic implementation regardless  whether `L` has an `__contains__` method or 
not. This behavior can be necessary if these functions are called from inside
method definitions in order to avoid infinite recurrence.
'''

if __name__ == '__main__':
    __package__ = 'listtools'  # @ReservedAssignment
    import listtools  # @UnusedImport

from .api_generics import is_generic

DEFAULT = object()
__all__ = ['getitem', 'setitem', 'delitem', 'pop', 'contains', 'hash_value',
           'isequal', 'delslice', 'getslice', 'insert', 'append', 'reverse',
           'extend', 'remove', 'index', 'sort', 'count']

def getitem(L, idx, default=DEFAULT):
    '''getitem(x, idx) <==> x[idx]
        
    If idx does not exist it returns the default value if it is given. 
    '''

    try:
        return L[idx]
    except IndexError:
        if default is DEFAULT:
            raise
        else:
            return default

def setitem(L, idx, value):
    '''setitem(x, idx, value) <==> x[idx] = value'''

    L[idx] = value

def delitem(L, idx):
    '''delitem(x, idx) <==> del x[idx]'''

    del L[idx]

@is_generic
def pop(L, idx=-1):
    '''pop(x, k[,d]) -> v, remove specified idx from x and return the corresponding
    value. If idx is not found, d is returned if given, otherwise KeyError is raised
    
    Examples
    --------
    
    >>> L = [1, 2, 3, 4]
    >>> pop(L), L
    (4, [1, 2, 3])
    '''

    value = L[idx]
    del L[idx]
    return value

@is_generic(method_name='__contains__')
def contains(L, value):
    '''contains(L, value) <==> value in L'''

    for v in L:
        if v == value:
            return True
    else:
        return False

@is_generic(method_name='__hash__')
def hash_value(L):
    '''A hash-function implementation for mappings. Mutable mappings may change
    its hash value upon mutation.
    
    Examples
    --------
    
    >>> L1 = [1,2,3,4]
    >>> L2 = [1,2,3,4]
    >>> L3 = [0,1,2,3]
    >>> hash_value(L1) == hash_value(L2)
    True
    >>> hash_value(L1) == hash_value(L3)
    False
    '''

    return hash(tuple(L))

@is_generic(method_name='__eq__')
def isequal(L, other):
    '''Check if two mappings are equal by comparing its idx, value pairs.
    
    >>> isequal([1,2,3], (1,2,3))
    True
    '''

    if len(L) != len(other):
        return False
    else:
        return all(x == y for (x, y) in zip(L, other))

@is_generic(method_name='__delslice__')
def delslice(L, i, j=None):
    '''delslice(L, i, j) <==> del L[i:j]
    
    Examples
    --------
    
    >>> L = list(range(10))
    >>> delslice(L, 2, 5); L
    [0, 1, 5, 6, 7, 8, 9]
    '''

    j = (j if j is not None else len(L) - 1)
    for _ in range(j - i):
        del L[i]

@is_generic(method_name='_getslice__')
def getslice(L, i=0, j=None):
    '''getslice(L, i, j) <==> L[i:j]
    
    Examples
    --------
    
    >>> getslice(range(10), 2, 5)
    [2, 3, 4]
    '''

    j = j or len(L)
    return [L[idx] for idx in range(i, j)]

@is_generic(method_name='_getslice__')
def setslice(L, i, j, value):
    '''getslice(L, i, j, value) <==> L[i:j] = value
    
    Examples
    --------
    
    >>> L = list(range(10))
    >>> setslice(L, 2, 5, [0, 0, 0]); L
    [0, 1, 0, 0, 0, 5, 6, 7, 8, 9]
    '''
    if len(value) != j - i:
        raise IndexError

    for idx, v in zip(range(i, j), value):
        L[idx] = v

def insert(L, idx, value):
    '''insert(L, index, object) -- insert object before index'''

    L.insert(idx, value)

@is_generic
def append(L, value):
    '''append(L, object) -- append object to end'''

    L.insert(len(L), value)

@is_generic
def reverse(L):
    '''reverse(L) -- reverse *IN PLACE*'''

    n = len(L)
    for i in range(n // 2):
        L[i], L[n - i - 1] = L[n - i - 1], L[i]

@is_generic
def extend(L, values):
    '''extend(L, iterable) -- extend list by appending elements from the iterable'''

    for v in values:
        L.append(v)

@is_generic
def remove(L, value):
    '''remove(L, value) -- remove first occurrence of value.
    Raises ValueError if the value is not present.'''

    del L[index(L, value)]

@is_generic
def index(L, value, start=0, stop=None):
    '''index(L, value, [start, [stop]]) -> integer -- return first index of value.
    Raises ValueError if the value is not present.
    
    Example
    -------
    
    >>> index([-2, -1, 0, 1, 2], 0)
    2
    '''

    stop = (len(L) if stop is None else stop)
    for i in range(start, stop):
        if L[i] == value:
            return i
    raise ValueError

@is_generic
def count(self, value):
    '''count(L, value) -> integer -- return number of occurrences of value'''

    return sum(1 for v in self if v == value)

@is_generic
def sort(L, key=None, reverse=False):  # @ReservedAssignment
    '''sort(L, key=None, reverse=False) -- stable sort *IN PLACE*;
    
    Example
    -------
    
    >>> L = [3, 2, 6, 1, 10]
    >>> sort(L); L
    [1, 2, 3, 6, 10]
    '''

    for idx, v in enumerate(sorted(L, key=key, reverse=reverse)):
        L[idx] = v

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
