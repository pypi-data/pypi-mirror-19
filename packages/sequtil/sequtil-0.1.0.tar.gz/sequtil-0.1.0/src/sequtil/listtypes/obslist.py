if __name__ == '__main__':
    __package__ = 'listtools.listtypes'  # @ReservedAssignment
    import listtools  # @UnusedImport

from .base import Sequence
from ..utilities import docs_from


@docs_from(list)
class obslist(Sequence):

    '''A list that implements the "Observer" pattern. It executes callback
    functions before performing changes such as insertions, deletions and
    changing items. Callbacks functions can also prevent these modifications
    from happening.

    Usage
    -----

    `obslist` objects behave like regular lists:

    >>> L = obslist(['ham', 'spam', 'foo'])
    >>> L[0];
    'ham'

    Additionaly, it is possible to register callbacks to monitor modifications
    to the list.

    >>> def handler(i, v):
    ...     print('handler called with (%s, %s)' % (i, v))

    This handler simply echoes its arguments. Let us register it to be executed
    after insertions.

    >>> L.register('post-insert', handler)
    >>> L.append('bar')
    handler called with (3, bar)

    The "pre-*" signals can be used to cancel modification to the list
    if the handler raises any exceptions. All exceptions are propagated, except
    StopIteration, which signalizes that the operation should be terminated
    silently.

    >>> def handler(i, v):
    ...     raise StopIteration
    >>> L.register('pre-insert', handler)
    >>> L.append('blah'); L
    obslist(['ham', 'spam', 'foo', 'bar'])

    It is the user's responsability to raise the appropriate exceptions in
    callback functions for cancelled operations if this is the desired
    behavior.
    '''

    def __init__(self, data, copy=False):
        self._data = list(data) if copy else data
        self._pre_setitem_cb = []
        self._post_setitem_cb = []
        self._pre_delitem_cb = []
        self._post_delitem_cb = []
        self._pre_insert_cb = []
        self._post_insert_cb = []

    # Sequence API functions ##################################################
    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, repr(self._data))

    def __delitem__(self, idx):
        try:
            self.pre_delitem(idx)
        except StopIteration:
            pass
        else:
            value = self._data[idx]
            del self._data[idx]
            self.post_delitem(idx, value)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return type(self)(self._data[idx], copy=False)
        return self._data[idx]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __setitem__(self, idx, value):
        try:
            self.pre_setitem(idx, value)
        except StopIteration:
            pass
        else:
            self._data[idx] = value
            self.post_setitem(idx, value)

    def __contains__(self, idx):
        return idx in self._data

    def insert(self, idx, value):
        try:
            self.pre_insert(idx, value)
        except StopIteration:
            pass
        else:
            self._data.insert(idx, value)
            self.post_insert(idx, value)

    def append(self, value):
        idx = len(self)
        try:
            self.pre_insert(idx, value)
        except StopIteration:
            pass
        else:
            self._data.append(value)
            self.post_insert(idx, value)

    # Control callbacks #######################################################
    def pre_insert(self, idx, value):
        '''Called before insertions. If it raises a StopIteration, the
        insertion operation is cancelled silently.'''

        for func in self._pre_insert_cb:
            func(idx, value)

    def post_insert(self, idx, value):
        '''Called just after insertions.

        The first exceptions raised by a callback will be propagated'''

        exceptions = []
        for func in self._post_insert_cb:
            try:
                func(idx, value)
            except Exception as ex:
                exceptions.append(ex)
        if exceptions:
            raise exceptions[0]

    def pre_setitem(self, idx, value):
        '''Called before setting an item. If it raises a StopIteration, the
        operation is cancelled silently.'''

        for func in self._pre_setitem_cb:
            func(idx, value)

    def post_setitem(self, idx, value):
        '''Called just after an item is modified.

        Exceptions raised by callbacks will be propagated'''

        exceptions = []
        for func in self._post_setitem_cb:
            try:
                func(idx, value)
            except Exception as ex:
                exceptions.append(ex)
        if exceptions:
            raise exceptions[0]

    def pre_delitem(self, idx):
        '''Called before deletions. If it raises a StopIteration, the deletion
        operation is cancelled silently.'''

        for func in self._pre_delitem_cb:
            func(idx)

    def post_delitem(self, idx, value):
        '''Called just after an item is deleted.

        Exceptions raised by callbacks will be propagated'''

        exceptions = []
        for func in self._post_delitem_cb:
            try:
                func(idx)
            except Exception as ex:
                exceptions.append(ex)
        if exceptions:
            raise exceptions[0]

    def register(self, signal, callback):
        '''Register callback for executing at the given signal. Signal can be
        any of 'pre-setitem', 'pre-delitem', 'pre-insert', 'post-setitem',
        'post-delitem', 'post-insert'.
        '''

        cb_map = ['pre-setitem', 'pre-delitem', 'pre-insert', 'post-setitem',
                  'post-delitem', 'post-insert']
        if signal not in cb_map:
            raise ValueError('signal not recognized: %r' % signal)

        attr = '_%s_cb' % signal.replace('-', '_')
        L = getattr(self, attr)
        L.append(callback)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
