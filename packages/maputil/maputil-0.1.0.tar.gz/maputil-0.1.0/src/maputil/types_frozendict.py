from dicttools.api_generics import copy_docstrings

__all__ = ['frozendict', 'frozenkeydict']


@copy_docstrings(dict)
class frozendict(dict):

    def __new__(cls, *args, **kwds):
        '''
        Immutable dictionary type

        frozendict():
            new empty dictionary.
        frozendict(mapping):
            new dictionary initialized from a mapping object's (key, value)
            pairs.
        frozendict(iterable):
            new dictionary initialized from ``{k: v for (k, v) in iterable}``.
        frozendict(**kwargs):
            new dictionary initialized with the ``name=value`` pairs in the
            keyword argument list.  For example: frozendict(one=1, two=2)

        Example
        -------

        >>> D = frozendict({'foo': 'bar', 'ham': 'spam'})
        >>> D['foo'] = 'bar'
        Traceback (most recent call last):
        ...
        KeyError: 'a frozendict cannot be modified.'


        ``fronzendict`` instances can be hashed if both key and values are
        hashable. They can be used as keys to dictionaries.

        >>> DD = {D: 'my dict'}

        '''
        return dict.__new__(cls, *args, **kwds)

    def __blocked(self, *args, **kwds):
        raise KeyError("a %s cannot be modified" % type(self).__name__)

    __delitem__ = __setitem__ = clear = pop = popitem = setdefault = update = \
        __blocked

    def __hash__(self):
        try:
            return self._cached_hash
        except AttributeError:
            h = self._cached_hash = hash(tuple(sorted(self.items())))
            return h

    def __repr__(self):
        return "frozendict(%s)" % (dict.__repr__(self)[1:-1])


class frozenkeydict(dict):

    def __new__(cls, *args, **kwds):
        '''
        Dictionary with immutable keys: the values associated to each key can
        be changed, but new keys cannot be added or deleted.


        Example
        -------

        >>> D = frozenkeydict({'foo': 'bar', 'ham': 'spam'})
        >>> D['foo'] = 'foobar'
        >>> D['bacon'] = 'eggs'
        Traceback (most recent call last):
        ...
        KeyError: 'cannot add new keys to frozenkeydict.'

        '''
        return dict.__new__(cls, *args, **kwds)

    def __blocked(self, *args, **kwds):
        tname = type(self).__name__
        raise KeyError('cannot add or remove keys of %s.' % tname)

    __delitem__ = clear = pop = popitem = __blocked

    def __setitem__(self, k, v):
        if k in self:
            dict.__setitem__(self, k, v)
        else:
            self.__blocked()

    def setdefault(self, k, v=None):
        if k in self:
            return self[k]
        else:
            self.__blocked()

    def update(self, E, **F):
        # Compute all keys that shall be added to the dictionary
        keys = self.replace()
        try:
            keys.update(E.keys())
        except AttributeError:
            keys.update(k for (k, _v) in E)
        keys.update(F)

        # Test if keys are valid
        if all(k in self for k in keys):
            dict.update(E, **F)
        else:
            self.__blocked()

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, dict.__repr__(self)[1:-1])

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
