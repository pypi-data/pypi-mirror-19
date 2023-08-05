import numpy as np

#===============================================================================
# UserArray base type
#===============================================================================
class UserArray(object):
    '''
    An array like interface that can be easier to subclass that numpy.ndarray.
    
    It delegates all implementations to the `_user_data` attribute of the 
    UserArray. This attribute holds the wrapped array.
    
    '''
    __slots__ = ['_user_data']

    def __init__(self, data):
        self._user_data = np.array(data)

    @classmethod
    def _from_array(cls, data):
        '''Constructs an UserArray object from some array data by assigining it
        to the _user_array attribute. If extra computation is necessary to
        correctly initialize the object, subclasses must define the 
        _from_array_init() method, which takes no arguments.'''

        new = object.__new__(cls)
        new._user_data = data
        new._from_array_init()
        return new

    def _from_array_init(self):
        '''Must be used in subclasses. The default implementation does 
        nothing'''
        pass

    def _wrap(self, res, dowrap=None):
        '''Wraps an array into a UserArray object'''

        if dowrap is None:
            if isinstance(res, np.ndarray):
                return self._from_array(res)
            else:
                return res
        elif dowrap:
            return self._from_array(res)
        else:
            return res

    def _unwrap(self, other):
        '''Unwraps a UserArray instance and return the array. If object is not
        an UserArray, return itself'''

        if isinstance(other, UserArray):
            return other._user_data
        else:
            return other

    #===========================================================================
    # Basic python protocol
    #===========================================================================
    def __repr__(self):
        tname = type(self).__name__
        pre, sep, data = repr(self._user_data).partition('(')
        if not sep:
            data = pre
        else:
            data = data.rstrip(')')
        return '%s(%s)' % (tname, data)

    def __str__(self):
        tname = type(self).__name__
        data = '\n    '.join(str(self._user_data).splitlines())
        return '%s() object:\n    %s' % (tname, data)

    #===========================================================================
    # Auto-generated or semi-auto generated methods
    #
    # All manually crafted methods should go before in order to avoid rewriting
    # them when auto-generating the wrapping.
    #===========================================================================
    # Regular ndarray API
    #===========================================================================
    def all(self, axis=None, out=None):
        return self._wrap(self._user_data.all(axis, out), None)

    def any(self, axis=None, out=None):
        return self._wrap(self._user_data.any(axis, out), None)

    def argmax(self, axis=None, out=None):
        return self._wrap(self._user_data.argmax(axis, out), None)

    def argmin(self, axis=None, out=None):
        return self._wrap(self._user_data.argmin(axis, out), None)

    def argpartition(self, kth, axis=-1, kind='introselect', order=None):
        return self._wrap(self._user_data.argpartition(kth, axis, kind, order), None)

    def argsort(self, axis=-1, kind='quicksort', order=None):
        return self._wrap(self._user_data.argsort(axis, kind, order), None)

    def astype(self, dtype, order='K', casting='unsafe', subok=True, copy=True):
        return self._wrap(self._user_data.astype(dtype, order, casting, subok, copy), None)

    def byteswap(self, inplace):
        return self._wrap(self._user_data.byteswap(inplace), None)

    def choose(self, choices, out=None, mode='raise'):
        return self._wrap(self._user_data.choose(choices, out, mode), None)

    def clip(self, a_min, a_max, out=None):
        return self._wrap(self._user_data.clip(a_min, a_max, out), None)

    def compress(self, condition, axis=None, out=None):
        return self._wrap(self._user_data.compress(condition, axis, out), None)

    def conj(self,):
        return self._wrap(self._user_data.conj(), None)

    def conjugate(self,):
        return self._wrap(self._user_data.conjugate(), None)

    def copy(self, order='C'):
        return self._wrap(self._user_data.copy(order), None)

    def cumprod(self, axis=None, dtype=None, out=None):
        return self._wrap(self._user_data.cumprod(axis, dtype, out), None)

    def cumsum(self, axis=None, dtype=None, out=None):
        return self._wrap(self._user_data.cumsum(axis, dtype, out), None)

    def diagonal(self, offset=0, axis1=0, axis2=1):
        return self._wrap(self._user_data.diagonal(offset, axis1, axis2), None)

    def dot(self, b, out=None):
        return self._wrap(self._user_data.dot(b, out), None)

    def dump(self, file):
        return self._wrap(self._user_data.dump(file), None)

    def dumps(self,):
        return self._wrap(self._user_data.dumps(), None)

    def fill(self, value):
        return self._wrap(self._user_data.fill(value), None)

    def flatten(self, order='C'):
        return self._wrap(self._user_data.flatten(order), None)

    def getfield(self, dtype, offset=0):
        return self._wrap(self._user_data.getfield(dtype, offset), None)

    def item(self, *args):
        return self._wrap(self._user_data.item(*args), None)

    def itemset(self, *args):
        return self._wrap(self._user_data.itemset(*args), None)

    def max(self, axis=None, out=None):
        return self._wrap(self._user_data.max(axis, out), None)

    def mean(self, axis=None, dtype=None, out=None):
        return self._wrap(self._user_data.mean(axis, dtype, out), None)

    def min(self, axis=None, out=None):
        return self._wrap(self._user_data.min(axis, out), None)

    def newbyteorder(self, new_order='S'):
        return self._wrap(self._user_data.newbyteorder(new_order), None)

    def nonzero(self,):
        return self._wrap(self._user_data.nonzero(), None)

    def partition(self, kth, axis=-1, kind='introselect', order=None):
        return self._wrap(self._user_data.partition(kth, axis, kind, order), None)

    def prod(self, axis=None, dtype=None, out=None):
        return self._wrap(self._user_data.prod(axis, dtype, out), None)

    def ptp(self, axis=None, out=None):
        return self._wrap(self._user_data.ptp(axis, out), None)

    def put(self, indices, values, mode='raise'):
        return self._wrap(self._user_data.put(indices, values, mode), None)

    def ravel(self, *args):
        if args:
            order = args[0]
            return self._wrap(self._user_data.ravel(order), None)
        else:
            return self._wrap(self._user_data.ravel(), None)

    def repeat(self, repeats, axis=None):
        return self._wrap(self._user_data.repeat(repeats, axis), None)

    def reshape(self, shape, order='C'):
        return self._wrap(self._user_data.reshape(shape, order), None)

    def resize(self, new_shape, refcheck=True):
        return self._wrap(self._user_data.resize(new_shape, refcheck), None)

    def round(self, decimals=0, out=None):
        return self._wrap(self._user_data.round(decimals, out), None)

    def searchsorted(self, v, side='left', sorter=None):
        return self._wrap(self._user_data.searchsorted(v, side, sorter), None)

    def setfield(self, val, dtype, offset=0):
        return self._wrap(self._user_data.setfield(val, dtype, offset), None)

    def setflags(self, write=None, align=None, uic=None):
        return self._wrap(self._user_data.setflags(write, align, uic), None)

    def sort(self, axis=-1, kind='quicksort', order=None):
        return self._wrap(self._user_data.sort(axis, kind, order), None)

    def squeeze(self, axis=None):
        return self._wrap(self._user_data.squeeze(axis), None)

    def std(self, axis=None, dtype=None, out=None, ddof=0):
        return self._wrap(self._user_data.std(axis, dtype, out, ddof), None)

    def sum(self, axis=None, dtype=None, out=None):
        return self._wrap(self._user_data.sum(axis, dtype, out), None)

    def swapaxes(self, axis1, axis2):
        return self._wrap(self._user_data.swapaxes(axis1, axis2), None)

    def take(self, indices, axis=None, out=None, mode='raise'):
        return self._wrap(self._user_data.take(indices, axis, out, mode), None)

    def tobytes(self, order='C'):
        return self._wrap(self._user_data.tobytes(order), None)

    def tofile(self, fid, sep="", format="%s"):
        return self._wrap(self._user_data.tofile(fid, sep, format), None)

    def tolist(self,):
        return self._wrap(self._user_data.tolist(), None)

    def tostring(self, order='C'):
        return self._wrap(self._user_data.tostring(order), None)

    def trace(self, offset=0, axis1=0, axis2=1, dtype=None, out=None):
        return self._wrap(self._user_data.trace(offset, axis1, axis2, dtype, out), None)

    def transpose(self, *axes):
        return self._wrap(self._user_data.transpose(*axes), None)

    def var(self, axis=None, dtype=None, out=None, ddof=0):
        return self._wrap(self._user_data.var(axis, dtype, out, ddof), None)

    def view(self, dtype=None, type=None):
        return self._wrap(self._user_data.view(dtype, type), None)

    #===========================================================================
    # Properties
    #===========================================================================
    @property
    def _noaccess(self):
        raise AttributeError('does not have direct access to wrapped array memory')
    base = ctypes = data = _noaccess

    @property
    def dtype(self):
        return self._user_data.dtype

    @property
    def flags(self):
        return self._user_data.flags

    @property
    def flat(self):
        return self._user_data.flat

    @property
    def imag(self):
        return self._user_data.imag

    @property
    def itemsize(self):
        return self._user_data.itemsize

    @property
    def nbytes(self):
        return self._user_data.nbytes

    @property
    def ndim(self):
        return self._user_data.ndim

    @property
    def real(self):
        return self._user_data.real

    @property
    def shape(self):
        return self._user_data.shape

    @property
    def size(self):
        return self._user_data.size

    @property
    def strides(self):
        return self._user_data.strides

    @property
    def T(self):
        return self._wrap(self._user_data.T)

    #===========================================================================
    # Binary operators
    #===========================================================================
    def __add__(self, value):
        return self._wrap(self._user_data + self._unwrap(value), None)

    def __and__(self, value):
        return self._wrap(self._user_data & self._unwrap(value), None)

    def __divmod__(self, value):
        return self._wrap(divmod(self._user_data, self._unwrap(value)), None)

    def __floordiv__(self, value):
        return self._wrap(self._user_data // self._unwrap(value), None)

    def __lshift__(self, value):
        return self._wrap(self._user_data << self._unwrap(value), None)

    def __mod__(self, value):
        return self._wrap(self._user_data % self._unwrap(value), None)

    def __mul__(self, value):
        return self._wrap(self._user_data * self._unwrap(value), None)

    def __or__(self, value):
        return self._wrap(self._user_data | self._unwrap(value), None)

    def __pow__(self, value, mod=None):
        return self._wrap(pow(self._user_data, self._unwrap(value), mod), None)

    def __rshift__(self, value):
        return self._wrap(self._user_data >> self._unwrap(value), None)

    def __sub__(self, value):
        return self._wrap(self._user_data - self._unwrap(value), None)

    def __truediv__(self, value):
        return self._wrap(self._user_data / self._unwrap(value), None)

    def __xor__(self, value):
        return self._wrap(self._user_data ^ self._unwrap(value), None)

    #===========================================================================
    # Inplace operators
    #===========================================================================
    def __iadd__(self, value):
        self._user_data += self._unwrap(value)
        return self

    def __iand__(self, value):
        self._user_data &= self._unwrap(value)
        return self

    def __ifloordiv__(self, value):
        self._user_data // self._unwrap(value)
        return self

    def __ilshift__(self, value):
        self._user_data <<= self._unwrap(value)
        return self

    def __imod__(self, value):
        self._user_data %= self._unwrap(value)
        return self

    def __imul__(self, value):
        self._user_data *= self._unwrap(value)
        return self

    def __ior__(self, value):
        self._user_data |= self._unwrap(value)
        return self

    def __ipow__(self, value):
        self._user_data **= self._unwrap(value)
        return self

    def __irshift__(self, value):
        self._user_data >>= self._unwrap(value)
        return self

    def __isub__(self, value):
        self._user_data -= self._unwrap(value)
        return self

    def __itruediv__(self, value):
        self._user_data / self._unwrap(value)
        return self

    def __ixor__(self, value):
        self._user_data ^= self._unwrap(value)
        return self

    #===========================================================================
    # Reverse binary operators
    #===========================================================================
    def __radd__(self, other):
        return self +other

    def __rand__(self, other):
        return self & other

    def __rdivmod__(self, other):
        other = self._unwrap(other)
        return self._wrap(divmod(other, self._user_data))

    def __rfloordiv__(self, other):
        other = self._unwrap(other)
        return self._wrap(other // self._user_data)

    def __rlshift__(self, other):
        other = self._unwrap(other)
        return self._wrap(other << self._user_data)

    def __rmod__(self, other):
        other = self._unwrap(other)
        return self._wrap(other % self._user_data)

    def __rmul__(self, other):
        return self * other

    def __ror__(self, other):
        return self._wrap(self | other)

    def __rpow__(self, other):
        other = self._unwrap(other)
        return self._wrap(other ** self._user_data)

    def __rrshift__(self, other):
        other = self._unwrap(other)
        return self._wrap(other >> self._user_data)

    def __rsub__(self, other):
        other = self._unwrap(other)
        return -self + other

    def __rtruediv__(self, other):
        other = self._unwrap(other)
        return self._wrap(other // self._user_data)

    def __rxor__(self, other):
        other = self._unwrap(other)
        return self._wrap(self ^ other)

    #===========================================================================
    # Array Interface
    #===========================================================================
    def __array_prepare__(self, array, context=None):
        return array

    def __array_wrap__(self, array, context=None):
        return self._wrap(array)

    def __array_priority__(self):
        return 1.0

    def __array__(self, dtype=None):
        return self._user_data

    #===========================================================================
    # Semi-manually written methods
    #===========================================================================
    def __getitem__(self, idx):
        return self._user_data.__getitem__(idx)

    def __setitem__(self, idx, value):
        return self._user_data.__setitem__(idx, value)

    def __delitem__(self, idx):
        return self._user_data.__delitem__(idx)

    def __abs__(self):
        return self._user_array.__abs__()

    def __bool__(self):
        return self._user_array.__bool__()

    def __contains__(self, value):
        return self._user_array.__contains__(value)

    def __copy__(self):
        return self._user_array.__copy__()

    def __deepcopy__(self, memo):
        return self._user_array.__deepcopy__(memo)

    def __float__(self):
        return self._user_array.__float__()

    def __index__(self):
        return self._user_array.__index__()

    def __int__(self):
        return self._user_array.__int__()

    def __invert__(self):
        return self._user_array.__invert__()

    def __iter__(self):
        return self._user_array.__iter__()

    def __len__(self):
        return self._user_array.__len__()

    def __neg__(self):
        return self._user_array.__neg__()

    def __pos__(self):
        return self._user_array.__pos__()

    def __setstate__(self, state):
        return self._user_array.__setstate__(state)

#===============================================================================
# Auxiliary functions for auto-generating the wrapping
#===============================================================================
GENERATE = False

def _guess_signature(func):
    '''Very crude function to try to guess the signature of a method. Looks at
    the docstrings'''

    name = func.__name__
    _, sep, args = func.__doc__.partition(name + '(')
    if not sep:
        print(func.__doc__)
        raise ValueError('could not find signature')

    sigf = args.partition(')')[0]
    args = [ a.partition('=')[0].strip() for a in sigf.split(',') ]
    return sigf, ', '.join(args)

def _is_bin_op(func):
    '''Try to guess if function is a binary operator'''

    return 'value' in func.__doc__

def _indent(src, indent):
    '''Indent source'''
    if indent:
        src = src.splitlines()
        src[0] = ' ' * indent + src[0]
        src = ('\n' + ' ' * indent).join(src)
    return src

def _mk_source(func, indent=0):
    '''Creates a source that wraps the given ndarray function'''

    sigf, sigc = _guess_signature(func)
    name = func.__name__
    src = ('\ndef {name}(self, {sigf}):\n'
           '    return self._wrap(self._user_data.{name}({sigc}), None)'
    ).format(name=name, sigf=sigf, sigc=sigc)
    return _indent(src, indent)

def _mk_bin_source(func, indent=0):
    '''Creates a source that wraps the given ndarray binary operator'''

    op = func.__doc__.splitlines()[-1][7:].strip('.')
    op = op.replace('self', 'self._user_data')
    op = op.replace('value', 'self._unwrap(value)')
    name = func.__name__
    src = ('\ndef {name}(self, value):\n'
           '    return self._wrap({op}, None)'
    ).format(name=name, op=op)
    return _indent(src, indent)

def _mk_iop_source(func, indent=0):
    '''Creates a source that wraps the given ndarray inplace operator'''

    op = func.__doc__.splitlines()[-1][7:].strip('.')
    op = op.replace('self', 'self._user_data')
    op = op.replace('value', 'self._unwrap(value)')
    name = func.__name__
    src = ('\ndef {name}(self, value):\n'
           '    {op}\n'
           '    return self'
    ).format(name=name, op=op)
    return _indent(src, indent)

def _mk_stub(func, indent):
    '''Creates a bare minimal skeleton that probably won't work, but helps 
    with less typing in a manual wrapping'''

    name = func.__name__
    src = ('\ndef {name}(self):\n'
           '    return self._user_array.{name}()'
    ).format(name=name)
    return _indent(src, indent)

if GENERATE:
    # This should never execute!
    import operator

    for attr in dir(np.ndarray):
        if not hasattr(UserArray, attr):
            func = getattr(np.ndarray, attr)
            if callable(func):
                if not attr.startswith('_'):
                    print(_mk_source(func, 4))
                elif _is_bin_op(func):
                    if attr[2] == 'i':
                        print(_mk_iop_source(func, 4))
                    else:
                        print(_mk_bin_source(func, 4))
                else:
                    print(_mk_stub(func, 4))
    print('\n'.join(sorted(set(dir(np.ndarray)) - set(dir(UserArray)))))

#===============================================================================
# Derived UserArray classes
#===============================================================================
class growarray(UserArray):
    '''An array-like object that can grow in an efficient manner.
    
    Example
    -------
    
    >>> A = growarray([1, 2, 3])
    >>> A.sum()
    6
    
    It accepts all the usual array operations, such as arithmetic and ufuncs
    
    >>> A + A**2
    growarray([ 2,  6, 12])
    >>> np.sin(A)
    growarray([ 0.84147098,  0.90929743,  0.14112001])
    
    Besides the regular array stuff, we can grow and shrink A easily
    
    >>> A.append(4)
    >>> A.extend([5, 6]); A
    growarray([1, 2, 3, 4, 5, 6])
    
    Deletions and insertions also works
    
    >>> A.insert(3, 0); A
    growarray([1, 2, 3, 0, 4, 5, 6])
    >>> del A[3]; A
    growarray([1, 2, 3, 4, 5, 6])
    
    Careful must be given to slicing. Slices may become out of sync after some 
    operation makes the array grow.  
    
    >>> B = A[:]; 
    >>> B[0] = 24       # This also change the value in A
    >>> A.extend([6, 7, 8, 9, 10])
    >>> B[0] = 42; A    # This doesn't since A had to allocate memory
    growarray([24,  2,  3,  4,  5,  6,  6,  7,  8,  9, 10])
    '''
    __slots__ = ['_N', '_base']

    def __init__(self, data):
        self._user_data = self._base = np.array(data)
        self._N = len(self._base)

    def _from_array_init(self):
        self._base = self._user_data
        self._N = len(self._base)

    def _alloc(self, size):
        '''Allocates more memory for the base array'''

        # Compute new shape
        shape = list(self.shape)
        shape[0] += size
        shape = tuple(shape)

        # Remove references and resize array
        del self._user_data

        try:
            self._base.resize(shape, refcheck=True)
        except ValueError:
            self._base = np.resize(self._base, shape)
            self._base[self._N:] *= 0
        self._update()

    def _update(self, N=None):
        '''Updates _user_data and _N to a new size N'''

        if N is None:
            N = self._N
        self._N = N
        self._user_data = self._base[:N]

    def grow(self):
        '''Allocates memory if needed to allow for the array to grow. I 
        allocates extra memory in chunks of half of the current size of the
        array'''

        newsize = max(self._N * 1.5, 10)
        if newsize > len(self._base):
            self._alloc(int(self._N / 2))

    def shrink(self):
        '''Free the current memory and reallocates so that the array wastes no 
        memory'''

        if self.wasted():
            shape = self.shape
            del self._user_data
            self._base.resize(shape)
            self._update()

    def wasted(self):
        '''Return the size of the wasted region. This size is the difference
        between the size of the allocated memory in the first index and the
        actual visible array'''

        return len(self._base) - self._N

    def reveal(self, size=1):
        '''Reveal the given size of elements from the allocated memory. Raises 
        an IndexError if outside the allocated memory region.'''

        if size > self.wasted():
            raise IndexError('trying to reveal a region larger than allocated memory')

    def append(self, value):
        '''Appends a value to the end of the array'''

        if len(self._base) > self._N:
            self._base[self._N] = value
            self._update(self._N + 1)
        else:
            self.grow()
            self.append(value)

    def extend(self, iterable):
        '''Extends the array with the given iterable'''

        N = self._N
        Nmax = len(self._base)
        try:
            Niter = len(iterable)
            Nend = N + Niter
            if Nend > Nmax:
                self._alloc(Niter)
            self._base[N:Nend] = iterable
            self._update(Nend)
        except TypeError:
            for i, x in enumerate(iterable):
                i += N
                if i >= Nmax - 1:
                    self.grow()
                    Nmax = len(self._base)
                self._base[i] = x
            self._update(i)

    def pop(self, idx=None):
        '''A.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if array is empty or index is out of range.'''

        # Pops last element
        if idx is None:
            res = self[-1]
            self._update(self._N - 1)

        # Pops specific element and adds to the list
        else:
            res = self[idx]
            del self[idx]

        return res

    def clear(self):
        '''Make the array empty'''

        self._update(0)

    def index(self, value, start=0, stop=-1):
        '''
        A.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.
        '''

        B = self._base
        if stop < 0:
            stop = self._N - stop
        for i in range(start, stop):
            if B[i] == value:
                return i
        else:
            raise ValueError('value not in array')

    def insert(self, idx, value):
        '''A.insert(index, object) -- insert object before index'''

        self.append(value)
        B = self._base
        for i in range(self._N - 2, idx - 1, -1):
            B[i + 1] = B[i]
        B[idx] = value

    def remove(self, value):
        '''
        A.remove(value) -> None -- remove first occurrence of value.
        Raises ValueError if the value is not present.
        '''

        del self[self.index(value)]

    def __delitem__(self, idx):
        B = self._base
        for i in range(idx, self._N - 1):
            B[i] = B[i + 1]
        self._update(self._N - 1)

    def __len__(self):
        return self._N

if __name__ == '__main__':
    import doctest
    doctest.testmod()

