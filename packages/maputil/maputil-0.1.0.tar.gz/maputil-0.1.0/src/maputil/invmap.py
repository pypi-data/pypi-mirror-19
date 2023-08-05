from lazyutils import lazy

from maputil import Mapping, inv
from maputil.util import copy_docstrings

__all__ = ['InvMap']


@copy_docstrings(dict)
class InvMap(Mapping):
    """
    A dictionary-like object with both a direct and inverse mapping.

    ``InvMap`` implements a invertible dictionary that can access `values`
    from `keys` as a regular dictionary, but it can also map `keys` to `values`.
    The inverse relation, which is also an ``InvMap`` instance, can be
    accessed from the ``inv`` attribute of the dictionary.

    Examples:
        Consider a map of natural numbers to their respective squares.

        >>> squares = InvMap((k, k**2) for k in range(5))
        >>> squares[2] # square of 2
        4
        >>> squares.inv[4] # number whose square is 4
        2

        The inverse of the inverse is the mapping itself

        >>> squares.inv.inv is squares
        True

        One can use all regular dict methods in order to edit the dictionary or
        its inverse, e.g.,

        >>> squares[5] = 25
        >>> squares.inv[36] = 6

        The inverse relation is simply an ``InvMap`` with the direct and
        reversed mappings exchanged

        >>> squares.inv
        InvMap({0: 0, 1: 1, 4: 2, 9: 3, 16: 4, 25: 5, 36: 6})

    Notes:
        Inspired on Josh Bronson's ``bidict`` module
        (http://pypi.python.org/pypi/bidict)
    """
    EMPTY = object()

    @lazy
    def inv(self):
        inv = object.__new__(InvMap)
        inv._direct, inv._inverse = self._inverse, self._direct
        inv.inv = self
        return inv

    def __init__(self, *args, **kwds):
        self._direct = dict(*args, **kwds)
        self._inverse = inv(self._direct)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, repr(self._direct))

    def __getitem__(self, key):
        return self._direct[key]

    def __len__(self):
        return len(self._direct)

    def __iter__(self):
        return iter(self._direct)

    def __setitem__(self, key, value):
        old_value = self.pop(key, self.EMPTY)

        if value in self._inverse:
            self._direct[key] = old_value
            self._inverse[old_value] = key
            raise ValueError('value exists: %s' % value)
        else:
            self._direct[key] = value
            self._inverse[value] = key

    def __delitem__(self, key):
        old_value = self._direct.pop(key, self.EMPTY)
        self._inverse.pop(old_value, self.EMPTY)

    def copy(self):
        new = object.__new__(type(self))
        new._direct, new._inverse = self._direct.copy(), self._inverse.copy()
        return new

    @classmethod
    def named(cls, class_name, direct, inverse):
        """
        Returns a ``InvMap`` subclass that have specially named attributes for
        direct and inverse access of the mapping relation.

        Examples:
            >>> Kings = InvMap.named('Kings', 'kings', 'realms')
            >>> x = Kings({'Pele': 'soccer', 'Elvis': "rock'n'roll"})
            >>> x.kings
            Kings({'Pele': 'soccer', 'Elvis': "rock'n'roll"})
            >>> x.realms
            InvMap({'soccer': 'Pele', "rock'n'roll": 'Elvis'})
        """

        @property
        def direct_p(self):
            return self

        @property
        def inverse_p(self):
            return self.inv

        return type(
            class_name, (InvMap,), {
                direct: direct_p, inverse: inverse_p})
