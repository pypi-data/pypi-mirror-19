from collections import deque as _deque, Sequence as _Sequence
from math import sqrt as _sqrt

from sequtil.api import index as _index


#
# Insertion and removal
#
def discard(seq, value):
    """Like remove, but does not raise errors if value is not present."""

    try:
        idx = _index(seq, value)
    except IndexError:
        pass
    else:
        del seq[idx]


def discard_n(seq, value, n=None):
    """
    Discard at most `n` occurrences of `value`. If `n` is not given, all
    occurrences will be removed.

    Examples:
        >>> L = [1, 0, 1, 0, 0, 1, 1, 0, 0]
        >>> discard_n(L, 0, 2); L
        [1, 1, 0, 1, 1, 0, 0]
        >>> discard_n(L, 1); L
        [0, 0, 0]
    """

    n = (n if n is not None else len(seq))
    idx = 0
    for _ in range(len(seq)):
        if seq[idx] == value:
            if n > 0:
                n -= 1
                del seq[idx]
            else:
                break
        else:
            idx += 1


def remove_items(seq, idx_list):
    """
    Remove all items in the given index list.

    Examples:
        >>> L = list(range(10))
        >>> remove_items(L, [2, 4, 9]); L
        [0, 1, 3, 5, 6, 7, 8]
    """

    idx_list = sorted(idx_list)
    if idx_list[-1] >= len(seq):
        raise IndexError(idx_list[-1])

    offset = 0
    for idx in idx_list:
        del seq[idx - offset]
        offset += 1


def insert_items(seq, items_list, idx_ref=1):
    """
    Insert items of the form (idx, value) in `items_list` by adding each value
    in the given index of the original list.

    Examples:
        By default, the indices refer to the indices in the original list.

        >>> L = [0, 1, 3, 5, 6, 7, 8, 9]
        >>> insert_items(L, [(2, 'two'), (3, 'four')]); L
        [0, 1, 'two', 3, 'four', 5, 6, 7, 8, 9]

        If, however, ``idx_ref=0`` this function performs the inverse of
        ``remove_items()``

        >>> remove_items(L, [2, 4])
        >>> insert_items(L, [(2, 'two'), (4, 'four')], idx_ref=0); L
        [0, 1, 'two', 3, 'four', 5, 6, 7, 8, 9]
    """

    items_list = list(sorted(items_list))
    if items_list[-1][0] >= len(seq):
        raise IndexError(items_list[-1][0])

    offset = 0
    for i, v in items_list:
        seq.insert(i + offset, v)
        offset += idx_ref


#
# Changing items
#
def set_items(seq, items_list):
    """
    Set the value of items of the form (idx, value) in `items_list`.

    Examples:
        >>> L = list(range(10))
        >>> set_items(L, [(2, 'two'), (4, 'four')]); L
        [0, 1, 'two', 3, 'four', 5, 6, 7, 8, 9]
    """

    items_list = list(sorted(items_list))
    if items_list[-1][0] >= len(seq):
        raise IndexError(items_list[-1][0])

    for i, v in items_list:
        seq[i] = v


#
# Zipping functions
#
def unzip(it):
    """
    Return N lists from the N components of each element of iterable `it`. This
    function invert the result of the zip() function.

    Examples:
        >>> a, b = unzip([(1,1), (2,4), (3,9)])
        >>> a, b
        ([1, 2, 3], [1, 4, 9])
    """

    it = iter(it)
    try:
        res = tuple([x] for x in next(it))
    except StopIteration:
        return []
    for item in it:
        if len(res) != len(item):
            break
        else:
            for (l, x) in zip(res, item):
                l.append(x)
    N = len(res[0])
    return tuple(x for x in res if len(x) == N)


def iunzip(it):
    """
    Similar to "unzip", but returns a list of N iterators from iterable it.

    Examples:
        >>> a, b = iunzip([(1,1), (2,4), (3,9)])
        >>> list(a), list(b)
        ([1, 2, 3], [1, 4, 9])
    """

    it = iter(it)
    consumed = [_deque([x]) for x in next(it)]
    size = len(consumed)
    stopped = [False]  # in a list so it can be modified by sub-iterators

    def make_iter(n):
        qi = consumed[n]
        while True:
            # Consume cache
            while qi:
                yield qi.popleft()

            # Check if main iterator has ended
            if stopped[0]:
                return

            # Extract the next object
            item = next(it)
            if len(item) == size:
                for i, v in enumerate(item):
                    consumed[i].append(v)
            else:
                stopped[0] = True
                return

    return tuple(make_iter(i) for i in range(size))


def zipfill(*iterables, value=None, values=None, fillfunc=None, size=None):
    """
    Similar to the `zip` built-in, but fill in empty values of the shorter
    iterators.

    It returns an iterator over tuples of (seq[0][i], seq[1][i], seq[2][i]...)
    Instead of truncating to the smaller iterator, `zipfill` fills missing
    elements.

    There are 3 possible methods for setting the fill-in values. Each is
    enabled by a specific keyword argument:

    value : anything
        If Fills all missing entries with this value.
    values : tuple
        A tuple of the same size as the number of iterators that fills a
        missing element of the i-th iterator with values[i].
    fillfunc : function
        A function fillfunc(i) --> tuple of values. Allows to compute the
        missing elements on-the-fly.

    The keyword `size` can be given to set the size of the resulting iterator.

    Examples:
        Consider the sequences

        >>> A = [1,2]; B = [1,2,3]; C = [1,2,3,4]

        The default fill-in value is None

        >>> Z = zipfill(A, B, C)
        >>> list(Z)
        [(1, 1, 1), (2, 2, 2), (None, 3, 3), (None, None, 4)]

        With the `values` keyword one set different fill-in values for each
        component of the zip.

        >>> Z = zipfill(A, B, C, values=('a', 'b', 'c'))
        >>> list(Z)
        [(1, 1, 1), (2, 2, 2), ('a', 3, 3), ('a', 'b', 4)]

        Finally, the fill-in value can be computed from the index of iteration

        >>> Z = zipfill(A, B, C, fillfunc=lambda i: (i + 1, i + 1, i + 1))
        >>> list(Z)
        [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4)]
    """

    N = len(iterables)

    # All behaviors can be replicated with the apropriate `fillfunc`
    if fillfunc is not None and values is None and value is None:
        pass
    elif values is not None and fillfunc is None and value is None:
        _values = values

        def fillfunc(i):
            return _values
    elif values is None and fillfunc is None:
        values = (value,) * N

        def fillfunc(i):
            return values
    else:
        raise ValueError("cannot set more than one of 'value', 'values' or "
                         "'fillfunc' simultaneously")

    # Safe next function
    errors = []

    def safe_next(running, it, idx):
        if running:
            try:
                return next(it)
            except StopIteration:
                errors.append(idx)
                return None
        else:
            return values[idx]

    # Creates the iterator that yields fill-up objects
    iters = [[True, iter(x)] for x in iterables]
    all_running = True
    idx = 0
    values = (None,) * N
    while idx < (size or float('inf')):
        if not all_running:
            values = fillfunc(idx)
        result = tuple(
            safe_next(
                run, it, i) for (
                i, (run, it)) in enumerate(iters))
        if errors:
            for error in errors:
                iters[error][0] = False
            if all_running:
                # the result value is wrong since "values" was not computed
                # and it is using the default value of None
                values = fillfunc(idx)
                result = list(result)
                for error in errors:
                    result[error] = values[error]
                result = tuple(result)

                # If size was not given, we must detect if iteration should
                # stop
                if size is None:
                    if not any(run for (run, it) in iters):
                        return

        yield result
        idx += 1


def zip_aligned(*args):
    """
    Similar to the zip built-in, but raises an ValueError if one sequence
    terminates before the others.
    """

    args = map(iter, args)
    yield from zip(*args)
    for idx, it in enumerate(args):
        try:
            next(it)
        except StopIteration:
            pass
        else:
            raise ValueError('the %s-th iterator is still running' % idx)


#
# Filtering functions
#
def filter_idx(func, seq):
    """
    Similar to the filter() built-in, but instead of returning the filtered
    values, return a list of the corresponding indexes.
    """

    func = bool if func is None else func
    return [i for (i, x) in enumerate(seq) if func(x)]


def separate(func, seq):
    """
    Similar to the built-in filter() function, but returns two sequences with
    the (filtered in, filtered out) values.

    Examples:
        >>> separate(lambda x: x % 3, [1, 2, 3, 4, 5, 6])
        ([1, 2, 4, 5], [3, 6])

        Respect the type of input sequence just as the filter() function

        >>> separate(lambda x: x.islower(), 'FoobAR')
        ('oob', 'FAR')
    """
    func = bool if func is None else func
    L1, L2 = [], []

    # Filter elements
    for x in seq:
        (L1 if func(x) else L2).append(x)

    # Return the right type
    if isinstance(seq, str):
        return ''.join(L1), ''.join(L2)
    elif isinstance(seq, tuple):
        return tuple(L1), tuple(L2)
    else:
        return L1, L2


def separate_idx(func, seq):
    """
    Similar to separate(), but return lists of indexes instead of values.
    """

    func = bool if func is None else func
    L1, L2 = [], []

    for i, x in enumerate(seq):
        (L1 if func(x) else L2).append(i)
    return L1, L2


#
# Sorting functions
#
def argsort(L, key=None, reverse=False):
    """Like the sorted() built-in, but return a list of indexes instead of
    values"""

    D = [(x, i) for (i, x) in enumerate(L)]
    if key:
        keyfunc = lambda x: key(x[0])
        D = sorted(D, reverse=reverse, key=keyfunc)
    else:
        D = sorted(D, reverse=reverse)
    return [i for (x, i) in D]


#
# Set functions
#
def intersection(*sets):
    """
    Return the intersection between all arguments.
    """

    first, *others = sets
    out = set(first)
    for other in others:
        out.intersection_update(other)
    return out


def union(*sets):
    """
    Return the union between all arguments.
    """

    first, *others = sets
    out = set(first)
    for other in others:
        out.update(other)
    return out


def unique(seq, exclude_repeated=False):
    """
    Return a list with unique values in list. The resulting list has the same
    ordering as L, but omits the repeated values.

    If the optional `exclude_repeated` argument is True, it only returns the
    values that were unique in the original list.

    Examples:
        >>> unique([1, 2, 3, 1])
        [1, 2, 3]
        >>> unique([1, 2, 3, 1], exclude_repeated=True)
        [2, 3]

    Notes:
        Differently from `set()`, elements do not need to be hashable.
    """
    if not exclude_repeated:
        unique = []
        for x in seq:
            if x not in unique:
                unique.append(x)
        return unique

    else:
        blacklist = repeated(seq)
        return [x for x in seq if x not in blacklist]


def unique_index(L, exclude_repeated=False):
    """
    Similar to `unique()`, but return the index of the first occurrence of
    each element.

    Examples:
        >>> L = [1, 2, 3, 1, 2, 4, 5]
        >>> unique_index([1, 2, 3, 1])
        [0, 1, 2]
        >>> unique_index([1, 2, 3, 1], exclude_repeated=True)
        [1, 2]
    """

    if not exclude_repeated:
        unique = []
        idx = []
        for i, x in enumerate(L):
            if x not in unique:
                unique.append(x)
                idx.append(i)
        return idx

    else:
        blacklist = repeated(L)
        return [i for i, x in enumerate(L) if x not in blacklist]


def repeated(seq):
    """
    Return a list with all elements in the list that occurs repeatedly.

    There is no predictable sorting in the output.

    Examples:
        >>> repeated([1, 2, 3, 2, 1])
        [2, 1]
    """
    repeated = []
    unique = []
    for x in reversed(seq):
        if x not in unique:
            unique.append(x)
        else:
            repeated.append(x)
    return repeated


def repeated_index(seq, first=True):
    """
    Return the indexes of all repeated elements.

    If `first=False` do not consider the first occurrence of each element.

    Examples:
        >>> repeated_index([1, 2, 1])
        [0, 2]
        >>> repeated_index([1, 2, 1, 2, 3], first=False)
        [2, 3]
    """

    if first:
        whitelist = repeated(seq)
        return [i for (i, x) in enumerate(seq) if x in whitelist]
    else:
        idx = []
        unique = []
        for i, x in enumerate(seq):
            if x in unique:
                idx.append(i)
            else:
                unique.append(x)
        return idx


def repeated_first(seq, *args):
    """
    Return the value first repetition in a list.

    Raises a ValueError if no repeated element is found and a second argument
    is not given.

    Examples:
        >>> repeated_first([1, 2, 2, 1])
        2
        >>> repeated_first([1, 2, 3], 'foo')
        'foo'
    """

    unique = []
    for x in seq:
        if x in unique:
            return x
        unique.append(x)

    if len(args) == 1:
        return args[0]
    elif len(args) == 0:
        raise ValueError('no repeated element in list')
    else:
        raise TypeError('only one or two arguments are accepted')


def repeated_first_index(seq):
    """
    Return the index first repetition in the list.

    Return None if no repeated value is found.

    Examples:
        >>> repeated_first_index([1, 2, 1, 2])
        2
    """

    unique = []
    for i, x in enumerate(seq):
        if x in unique:
            return i
        unique.append(x)

    return None


#
# Statistical functions
#
def count_all(seq, reverse=None):
    """
    Return a list of (value, count) pairs for each unique value in L.

    The result can be sorted from the least frequent to the most frequent if
    `reverse=False` or otherwise if reverse=True`.

    Examples:
        >>> count_all([10, 20, 10, 20, 30, 20], reverse=True)
        [(20, 3), (10, 2), (30, 1)]
    """

    # Assumes that items are hashable and proceed with counting
    countD = {}
    for idx, x in enumerate(seq):
        try:
            countD[x] = countD.get(x, 0) + 1
        except TypeError:
            break
    else:
        idx = None
    out = list(countD.items())

    # Resume filling up the list from where it left
    if idx is not None:
        countL = list(countD.items())
        for i in range(idx, len(seq)):
            x = seq[i]
            for i, (y, c) in enumerate(countL):
                if y == x:
                    out[i] = (x, c + 1)
                    break
            else:
                out.append((x, 1))

    # Sort and return
    if reverse is not None:
        out.sort(key=lambda x: x[1], reverse=reverse)
    return out


def mean(seq):
    """Return the mean of all values from seq."""

    try:
        N = float(len(seq))
        return sum(seq) / N

    # This works with iterators
    except TypeError:
        N = S = 0.0
        for x in seq:
            N += 1
            S += x
        return S / N


def var(seq):
    """Return the variance of all values from seq."""

    # This works with iterators
    N = S = S2 = 0.0
    for x in seq:
        N += 1
        S += x
        S2 += x ** 2

    return S2 / N - (S / N) ** 2


def std(seq):
    """Return the standard deviation of all values from seq."""

    return _sqrt(var(seq))


#
# Shape changing
#
def concatenate(item_or_sequences, *others):
    """
    Return a list with the concatenation of all given seqs

    Examples:
        There are two signatures:

        >>> a = [1, 2, 3]; b = [4, 5, 6]; c = [7, 8, 9]
        >>> concatenate(a, b, c)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> concatenate([a, b, c])
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """

    # Normalize arguments
    size = 0
    pre_list = ()
    seqs = item_or_sequences
    if others:
        size = len(item_or_sequences)
        seqs = others
        pre_list = item_or_sequences

    # Check if seqs is an iterator or a real sequence
    # (iterators can be consumed only once, so we need to change our strategy)
    if not isinstance(seqs, _Sequence):
        out = list(pre_list)
        for seq in seqs:
            out.extend(seq)
        return out

    # Get final size of concatenation
    for i, seq in enumerate(seqs):
        try:
            size += len(seq)
        except TypeError:
            seq = seqs[i] = list(seq)
            size += len(seq)
    out = [None] * size

    # Save items
    idx = len(pre_list)
    out[:idx] = pre_list
    for seq in seqs:
        size = idx + len(seq)
        out[idx:size] = seq
        idx = size
    return out


def flatten(data, level=float('inf'), types=list):
    """
    Flatten a structure of arbitrary nesting made with lists within lists.

    Args:
        data:
            A list with (possibly) nested list elements
        level (int):
            The maximum nesting level to flatten. If None (default), unest
            undefinetly.
        types (type or tuple of types):
            Types supposed to be flattened (defaults to list).

    Examples:
        >>> L = [1, [2, [3, 4]], (5, 6), 7]
        >>> flatten(L)
        [1, 2, 3, 4, (5, 6), 7]
        >>> flatten(L, types=(list, tuple))
        [1, 2, 3, 4, 5, 6, 7]
        >>> flatten(L, level=1, types=(list, tuple))
        [1, 2, [3, 4], 5, 6, 7]
    """

    if level >= 1:
        out = []
        for x in data:
            if isinstance(x, types):
                out.extend(flatten(x, level - 1, types))
            else:
                out.append(x)
        return out
    elif level == 0:
        return list(data)
    elif level < 0:
        raise ValueError('level cannot be negative')


###############################################################################
#                             Multidimensional
###############################################################################


def iloc(L, *args):
    """Get item by a multi-index from a multidimensional list of lists

    Example
    -------

    >>> L = [[0, 1, 2],
    ...      [3, 4, 5]]
    >>> iloc(L, 0, 0)
    0

    The function also accepts None arguments in order to take slices

    >>> iloc(L, None, 1)
    [1, 4]

    >>> iloc(L, 1, None)
    [3, 4, 5]
    """

    curr = L
    for i, idx in enumerate(args):
        if idx is not None:
            curr = curr[idx]
        else:
            base = args[:i]
            left = args[i + 1:]
            if left and base:
                return [iloc(L, *(base + (j,) + left))
                        for j in range(len(curr))]
            elif base:
                return [iloc(L, *(base + (j,))) for j in range(len(curr))]
            elif left:
                return [iloc(L, *((j,) + left)) for j in range(len(curr))]
            else:
                return [iloc(L, j) for j in range(len(curr))]
    else:
        return curr


def shape(seq, strict=False, types=(list, tuple)):
    """
    Return the shape of a list of lists.

    Examples:
        >>> L = [[0, 1, 2],
        ...      [3, 4, 5]]
        >>> shape(L,)
        (2, 3)
    """

    shape = []
    curr = seq
    if not strict:
        while isinstance(curr, types):
            shape.append(len(curr))
            try:
                curr = curr[0]
            except IndexError:
                break
    else:
        return NotImplemented

    return tuple(shape)
