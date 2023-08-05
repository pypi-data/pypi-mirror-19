'''
Module for random utility functions that are used internally in listtools
'''


def docs_from(source, destination=None):
    '''Fill docstrings for all methods in the destination class with those of
    the source class'''

    # Called in the decorator form
    if destination is None:
        def decorator(destination):
            docs_from(source, destination)
            return destination
        return decorator

    for attr in dir(destination):
        dobj = getattr(destination, attr, None)
        sobj = getattr(source, attr, None)
        if dobj is not None and dobj.__doc__ is None:
            if sobj is not None and sobj.__doc__ is not None:
                try:
                    dobj.__doc__ = sobj.__doc__
                except AttributeError:
                    pass

