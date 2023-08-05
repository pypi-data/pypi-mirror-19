from itertools import product
from dicttools.types_base import Mapping
from dicttools.api_generics import copy_docstrings

__all__ = ['MultiMap', 'iMultiMap', 'is_independent']


@copy_docstrings(dict)
class MultiMap(Mapping):

    '''A mapping from one key to many values.

    Basic usage
    -----------

    The MultiMap can be created from a list of pairs or another dict.

    >>> D = MultiMap([(0, 1), (0, 2), (1, 3), (2, 4), (2, 5), (2, 6)]); D
    MultiMap(0: (1, 2), 1: 3, 2: (4, 5, 6))

    Instead of mapping a key to a single element, it maps to a tuple
    (for which one is_connected no control of ordering)

    >>> D[0]
    (1, 2)

    Item assignment simply add elements to the mapping

    >>> D[0] = 3; D[0]
    (1, 2, 3)

    We can have finer-grained deletions, by specifying the complete mapping,
    or coarser grained one using only the key.

    >>> del D[0, 1]; D
    MultiMap(0: (2, 3), 1: 3, 2: (4, 5, 6))

    >>> del D[0]; D
    MultiMap(1: 3, 2: (4, 5, 6))


    Iterations
    ----------

    There are many ways to iterate over a MultiMap. The regular iterator
    iterates over keys, without repetitions.

    >>> list(D)
    [1, 2]

    The items() iterate over all associations, repeating keys when necessary

    >>> list(D.items())
    [(1, 3), (2, 4), (2, 5), (2, 6)]

    The methods keys() and values() just return the key and value part of each
    item. Keys and values are guaranteed to be synchronized like in regular
    dictionaries

    >>> list(D.keys())
    [1, 2, 2, 2]
    >>> list(D.values())
    [3, 4, 5, 6]

    Other methods have a slightly different behavior in order to make a dict
    like API work for an object that represents multiple arbitrary
    associations. For instance, the optional argument of get() and pop() must
    be a sequence.

    >>> D.get(3)
    ()
    >>> D.pop(0, range(3))
    (0, 1, 2)
    >>> D.pop(0, None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not iterable


    The popitem() method returns a random association. One can empty the
    MultiMap by calling it a sufficient number of times

    >>> for _ in range(4):
    ...     D.popitem()
    (1, 3)
    (2, 6)
    (2, 5)
    (2, 4)
    >>> D
    MultiMap()
    '''

    def __init__(self, *args, **kwds):
        self._data = {}
        self.update(*args, **kwds)

    @classmethod
    def full(cls, keys, values):
        '''Creates a new MultiMap object in which all keys and values are
        fully is_connected'''

        new = object.__new__(cls)
        new._data = {}
        new.update(product(keys, values))
        return new

    def __eq__(self, other):
        if other is self:
            return True
        elif isinstance(other, MultiMap):
            other = other._data
            if len(self._data) != len(other):
                return False
            for k, v in self._data.items():
                if k in other:
                    w = other[k]
                else:
                    return False
                if len(w) != len(v):
                    return False
                if any(x not in v for x in w):
                    return False
            return True
        else:
            return False

    def __repr__(self):
        L = []
        for k, v in self._data.items():
            v = tuple(v) if len(v) > 1 else repr(next(iter(v)))
            L.append('%r: %s' % (k, v))
        return '%s(%s)' % (type(self).__name__, ', '.join(L))

    def __getitem__(self, key):
        return tuple(self._data[key])

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __setitem__(self, key, value):
        try:
            L = self._data[key]
            if value not in L:
                L.append(value)
        except KeyError:
            self._data[key] = [value]

    def __delitem__(self, key):
        if isinstance(key, tuple):
            key, x = key
            S = self._data[key]
            try:
                S.remove(x)
            except:
                raise KeyError(key, x)
            if not S:
                del self._data[key]
        else:
            del self._data[key]

    def setitems(self, key, values):
        '''Set many items in batch.

        Equivalent to ``for v in values: D[key] = v``'''

        L = self._data.setdefault(key, [])
        for v in values:
            if v not in L:
                L.append(v)

    def get(self, key, default=()):
        '''Return all associations for the given key, otherwise returns a
        default tuple of associations.'''

        try:
            return tuple(self.data[key])
        except:
            return tuple(default)

    def pop(self, key, *args):
        return tuple(self._data.pop(key, *args))

    def popitem(self, *, full=False):
        key, S = self._data.popitem()
        if full:
            return key, tuple(S)
        else:
            value = S.pop()
            if S:
                self._data[key] = S
            return key, value

    def items(self):
        for k, s in self._data.items():
            for x in s:
                yield (k, x)

    def keys(self):
        for k, s in self._data.items():
            for _ in s:
                yield k

    def values(self):
        for s in self._data.values():
            yield from s

    def unique_keys(self):
        '''Iterates over unique keys'''

        return iter(self._data)

    def unique_values(self):
        '''Iterates over unique values'''

        hashable = set()
        non_hashable = []

        for values in self._data.values():
            try:
                hashable.update(values)
            except TypeError:
                for v in values:
                    try:
                        hashable.add(v)
                    except TypeError:
                        if v not in non_hashable:
                            non_hashable.append(v)
        yield from hashable
        yield from non_hashable

    def copy(self):
        new = object.__new__(type(self))
        new._data = {k: v.copy() for (k, v) in self._data.items()}
        return new

    def clear(self):
        self._data.clear()

    def update(self, data=(), **kwds):
        D = self._data

        if isinstance(data, MultiMap):
            for k, v in data._data.items():
                try:
                    L = D[k]
                except KeyError:
                    L = D[k] = []
                for x in v:
                    if x not in L:
                        L.append(v)
        else:
            items = getattr(data, 'items', lambda: data)
            for k, v in items():
                try:
                    L = D[k]
                    if v not in L:
                        L.append(v)
                except KeyError:
                    D[k] = [v]

        if kwds:
            self.update(kwds)

    def shape(self, unique=True):
        '''Return a tuple with (number_of_keys, number_of_values).

        If unique=True (default), consider only the unique values.'''

        D = self._data
        if unique:
            return (len(D), self.numvalues())
        else:
            return (len(D), self.numconnections())

    def numkeys(self):
        return len(self._data)

    def numvalues(self):
        return len(self.unique_values())

    def numconnections(self):
        return sum(map(len, self._data.values()))

    def sorted_keys(self):
        '''Return a sorted list of keys'''

        return sorted(self.unique_keys())

    def sorted_values(self):
        '''Return a sorted list of values'''

        return sorted(self.unique_values())

    def to_matrix(self, func=None, *, null=None):
        '''Applies func(a, b) to all (a, b) pairs in the MultiMap and present
        the results as a matrix which is ordered row-wise with by sorted keys
        and column-wise by sorted values.

        The optional null argument controls the value to be assigned to
        non-existing pairs. If no function is given, it simply echoes the
        arguments.

        Example
        -------

        >>> D = MultiMap([(0, 0), (0, 1), (1, 1), (2, 2)])
        >>> D.to_matrix()
        [[(0, 0), (0, 1), None], [None, (1, 1), None], [None, None, (2, 2)]]
        >>> D.to_matrix(lambda x, y: x + y, null=0)
        [[0, 1, 0], [0, 2, 0], [0, 0, 4]]
        '''

        out = []
        func = func or (lambda a, b: (a, b))
        D = self._data
        keys = self.sorted_keys()
        values = self.sorted_values()
        for k in keys:
            row = D[k]
            L = []
            out.append(L)
            for v in values:
                L.append(func(k, v) if v in row else null)
        return out

    def from_matrix(self, M, func=bool):
        '''Return a new MultiMap by selecting all pairs from a given matrix in
        which the test function yields True. If the test function is not given,
        it simply test the truth value of each element in the matrix.

        Example
        -------

        >>> D = MultiMap([(0, 0), (0, 1), (1, 1), (2, 2)])
        >>> M = D.to_matrix(lambda x, y: x + y, null=0); M
        [[0, 1, 0], [0, 2, 0], [0, 0, 4]]

        It will break the connection (0, 0) since it yields 0 in the matrix M

        >>> D.from_matrix(M)
        MultiMap(0: 1, 1: 1, 2: 2)
        '''

        new = type(self)()
        keys = self.sorted_keys()
        values = self.sorted_values()
        for i, k in enumerate(keys):
            for j, v in enumerate(values):
                if func(M[i][j]):
                    new[k] = v
        return new

    def is_simple(self):
        '''Return True if all keys are associated with a single value.

        Example
        -------

        >>> D = MultiMap({0: 1, 1: 2})
        >>> D.is_simple()
        True
        >>> D[0] = 2; D
        MultiMap(0: (1, 2), 1: 2)
        >>> D.is_simple()
        False
        '''

        return all(len(v) == 1 for v in self._data.values())

    def is_atomic(self):
        '''Return True if it represents an atomic association.

        An atomic association connects all keys to a single value or the other
        way around.

        Example
        -------

        >>> MultiMap([(0, 1), (0, 2)]).is_atomic()
        True
        >>> MultiMap([(0, 1), (2, 1)]).is_atomic()
        True
        >>> MultiMap([(0, 1), (1, 2)]).is_atomic()
        False
        '''

        if len(self._data) <= 1:
            return True

        values = iter(self.values())
        v0 = next(values)
        for v in values:
            if v != v0:
                return False
        return True

    def is_connected(self, a, b):
        '''Return True if mapping a -> b is present in the MultiMap'''

        try:
            return b in self._data[a]
        except KeyError:
            return False


class iMultiMap(MultiMap):

    '''An invertible MultiMap.

    It requires that both keys and values are hashable. iMultiMap are also
    slightly faster than MultiMap objects.'''

    @classmethod
    def full(cls, keys, values):
        '''Creates a new MultiMap in which all the given keys are is_connected to all
        the given values

        Example
        -------

        >>> D = iMultiMap.full(('a', 'b'), (1, 2))
        >>> D.to_matrix()
        [[('a', 1), ('a', 2)], [('b', 1), ('b', 2)]]
        '''
        keys = set(keys)
        values = set(values)
        new = object.__new__(cls)
        new._data = {k: values.copy() for k in keys}
        return new

    def __setitem__(self, key, value):
        try:
            self._data[key].add(value)
        except KeyError:
            self._data[key] = {value}

    def update(self, data=(), **kwds):
        D = self._data

        if isinstance(data, MultiMap):
            for k, v in data._data.items():
                try:
                    D[k].update(v)
                except KeyError:
                    D[k] = set(v)
        else:
            items = getattr(data, 'items', lambda: data)
            for k, v in items():
                try:
                    D[k].add(v)
                except KeyError:
                    D[k] = {v}

        if kwds:
            self.update(kwds)

    def setitems(self, key, values):
        '''Set many items in batch'''

        try:
            self._data[key].update(values)
        except KeyError:
            self._data[key] = set(values)

    def inv(self):
        '''Return another MultiMap which inverts the role of all (key, value)
        pairs

        Example
        -------

        >>> D = iMultiMap([(0, 0), (0, 1), (1, 1), (2, 2)])
        >>> D.inv()
        iMultiMap(0: 0, 1: (0, 1), 2: 2)
        >>> D.inv().inv() == D
        True
        '''

        return iMultiMap((v, k) for (k, v) in self.items())

    def unique_keys(self):
        '''Return a set of unique keys'''

        return set(self._data.keys())

    def unique_values(self):
        '''Return a set of unique values'''

        unique = set()
        for v in self._data.values():
            unique.update(v)
        return unique

    def decompose(self):
        '''Return a list of MultiMap objects in which the associations form
        a closed graph

        Example
        -------

        >>> D = iMultiMap([(0, 0), (0, 1), (1, 1), (2, 2)])
        >>> D.decompose()
        [iMultiMap(0: (0, 1), 1: 1), iMultiMap(2: 2)]

        '''

        inv = self.inv()
        out = []
        keys = set(self.keys())

        while keys:
            D = iMultiMap()
            curr_keys = {keys.pop()}

            while curr_keys:
                key = curr_keys.pop()
                D._data[key] = self._data[key]
                for v in self._data[key]:
                    S = inv._data[v]
                    curr_keys.update(S)
                    keys.difference_update(S)
                curr_keys.difference_update(D._data)

            out.append(D)

        assert is_independent(out)
        return out


def is_independent(L):
    '''Return True if all mappings in the list are decomposed into independent
    subgroups, i.e., no key and no value are shared between two different
    groups.'''

    keys = []
    values = []
    for g in L:
        keys.extend(g.unique_keys())
        values.extend(g.unique_values())
    return (len(values) == len(set(values))) and (len(keys) == len(set(keys)))


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
