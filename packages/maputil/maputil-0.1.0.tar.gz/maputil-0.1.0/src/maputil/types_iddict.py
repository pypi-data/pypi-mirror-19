from dicttools.types_base import Mapping
from dicttools.api_generics import copy_docstrings

__all__ = ['iddict']


@copy_docstrings(dict)
class iddict(Mapping, dict):

    '''A dictionary that handle keys by identity, not value.

    Keys of an `iddict` can be non-hashable types. Two keys that have the
    same value, but different identities are considered to be different keys.

    >>> D = iddict()
    >>> D[[1, 2]] = 3; D
    iddict({[1, 2]: 3})
    '''

    def __init__(self, iterable=(), **kwds):
        dict.__init__(self)
        self._objects = {}
        self.update(iterable, **kwds)

    def __delitem__(self, key):
        id_key = id(key)
        try:
            dict.__delitem__(self, id_key)
            del self._objects[id_key]
        except KeyError:
            raise KeyError(key)

    def __getitem__(self, key):
        return dict.__getitem__(self, id(key))

    def __iter__(self):
        return iter(self._objects.values())

    def __setitem__(self, key, value):
        id_key = id(key)
        dict.__setitem__(self, id_key, value)
        self._objects[id_key] = key

    def __repr__(self):
        name = type(self).__name__
        data = ', '.join('%s: %s' % item for item in self.items())
        return '%s({%s})' % (name, data)

    def __contains__(self, key):
        return dict.__contains__(self, id(key))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
