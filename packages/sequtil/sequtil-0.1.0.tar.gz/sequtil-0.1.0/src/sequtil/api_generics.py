import functools
import itertools

__all__ = ['is_generic', 'copy_docstrings']
NOT_GIVEN = object()


def is_generic(
        generic_implementation=NOT_GIVEN,
        method_name=None,
        args_ommit=NOT_GIVEN):
    """
    A generic implementation tries to use the appropriate method with its first
    argument, when available. Otherwise, the generic implementation is called.

    Examples:

        Consider the generic implementation for the `union` function of sets
        that also works in lists. The generic function tries to dispatch the
        work to the ``.union()`` method of the callee. Only if it does not exist
        that the generic implementation is used.

        >>> @generic
        ... def union(x, y):
        ...     print('using generic implementation...')
        ...     used = set()
        ...     result = []
        ...     for item in list(x) + list(y):
        ...         if item not in used:
        ...             used.add(item)
        ...             result.append(item)
        ...     return type(x)(result)

        The generic function works on lists, tuples, etc. It is only called if
        the first argument does not have a method with the same name as the
        generic function.

        The generic implementation is used for lists

        >>> union([1, 2, 3, 4], [4, 5])
        using generic implementation...
        [1, 2, 3, 4, 5]

        It is not used for sets, and the `union` method is called.

        >>> union(set([1, 2, 3, 4]), set([4, 5]))
        {1, 2, 3, 4, 5}

        One can force the use of the generic implementation by using the
        `.generic` attribute of the function.

        >>> union.generic(set([1, 2, 3, 4]), set([4, 5]))
        using generic implementation...
        set([1, 2, 3, 4, 5])
    """

    if generic_implementation is NOT_GIVEN:
        return functools.partial(
            is_generic,
            method_name=None,
            args_ommit=args_ommit)

    method_name = method_name or generic_implementation.__name__

    @functools.wraps(generic_implementation)
    def decorated(obj, *args, **kwds):
        try:
            method = getattr(type(obj), method_name)
        except AttributeError:
            return generic_implementation(obj, *args, **kwds)
        else:
            if args_ommit is not NOT_GIVEN:
                args = itertools.takewhile(lambda x: x is not NOT_GIVEN, args)
            return method(obj, *args, **kwds)

    decorated.generic = generic_implementation

    return decorated


def copy_docstrings(cls, orig=None):
    """
    Copy the docstrings from orig to cls, when no docstrings were provided
    """

    if orig is None:
        def decorator(x):
            copy_docstrings(x, cls)
            return x
        return decorator

    else:
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if attr.__doc__ is None:
                try:
                    attr.__func__.__doc__ = getattr(orig, attr_name).__doc__
                except AttributeError:
                    pass
