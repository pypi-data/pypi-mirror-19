import sys
from sequtil.api_generics import is_generic

NOT_GIVEN = object()
__all__ = ['getitem', 'setitem', 'delitem', 'pop', 'popitem', 'clear', 'update',
           'setdefault', 'contains', 'keys', 'values', 'items', 'hash_value',
           'isequal']


#
# Dictionary Mix-in methods
#
def getitem(D, key, default=NOT_GIVEN):
    """
    getitem(x, key) <==> x[key]

    If key does not exist it returns the default value if it is given.
    """

    try:
        return D[key]
    except KeyError:
        if default is NOT_GIVEN:
            raise
        else:
            return default


def setitem(D, key, value):
    """setitem(x, key, value) <==> x[key] = value"""

    D[key] = value


def delitem(D, key):
    """delitem(x, key) <==> del x[key]"""

    del D[key]


#
# Dictionary API
#
@is_generic(args_ommit=NOT_GIVEN)
def pop(D, key, default=NOT_GIVEN):
    """
    pop(x, k[,d]) -> v, remove specified key from x and return the corresponding
    value. If key is not found, d is returned if given, otherwise KeyError is
    raised.

    Examples:
        >>> D = {'foo': 'bar', 'ham': 'spam'}
        >>> pop(D, 'foo'), D
        ('bar', {'ham': 'spam'})
        >>> pop(D, 'eggs', 'bacon')
        'bacon'
    """

    try:
        value = D[key]
    except KeyError:
        if default is NOT_GIVEN:
            raise
        return default
    else:
        del D[key]
        return value


def _popitem_generic(D, default=NOT_GIVEN):
    # Generic implementation for popitem
    try:
        key = next(iter(D))
    except StopIteration:
        if default is NOT_GIVEN:
            raise KeyError
        else:
            return default
    else:
        value = D[key]
        del D[key]
        return (key, value)


def popitem(D, default=NOT_GIVEN):
    """
    popitem(x[,d]) -> (k, v), remove and return some (key, value) pair as a
    2-tuple; If x is empty, d is returned if given, otherwise KeyError is raised

    Examples:
        >>> popitem({'ham': 'spam'})
        ('ham', 'spam')
    """

    try:
        popitem = D.popitem
    except AttributeError:
        return _popitem_generic(D, default)
    else:
        try:
            return popitem()
        except KeyError:
            if default is NOT_GIVEN:
                raise
            else:
                return default


popitem.generic = _popitem_generic


@is_generic
def clear(D):
    """clear(D) -> None.  Remove all items from D."""
    try:
        while True:
            popitem(D)
    except KeyError:
        pass


@is_generic
def update(D, other=(), **kwds):
    """
    update(D, [E, ]**F) -> None.  Update D from dict/iterable E and F.
    If E present and has a .keys() method, does: for k in E: D[k] = E[k]
    If E present and lacks .keys() method, does: for (k, v) in E: D[k] = v
    In either case, this is followed by: for k in F: D[k] = F[k]
    """

    if hasattr(other, 'keys'):
        for key in other:
            D[key] = other[key]
    else:
        for key, value in other:
            D[key] = value
    for key, value in kwds.items():
        D[key] = value


@is_generic
def setdefault(D, key, default=None):
    """D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D"""

    try:
        return D[key]
    except KeyError:
        D[key] = default
    return default


@is_generic(method_name='__contains__')
def contains(D, key):
    """contains(D, key) <==> key in D"""

    try:
        D[key]
    except KeyError:
        return False
    else:
        return True


@is_generic(method_name='__hash__')
def hash_value(D):
    """
    A hash-function implementation for mappings. Mutable mappings may change
    its hash value after mutation. Use with care.

    Examples:
        >>> D1 = {'foo': 'bar', 'ham': 'spam'}
        >>> D2 = {'foo': 'bar', 'ham': 'spam'}
        >>> D3 = {'foo': 'bar', 'ham': 'eggs'}
        >>> hash_value(D1) == hash_value(D2)
        True
        >>> hash_value(D1) == hash_value(D3)
        False
    """

    hash_v = 0
    for item in items(D):
        hash_v |= hash(item)

    return hash_v


@is_generic(method_name='__eq__')
def isequal(D, other):
    """Check if two mappings are equal by comparing its key, value pairs."""

    other = dict(items(other))
    for key, value in items(D):
        if value != other.pop(key):
            return False
    else:
        return not bool(other)


@is_generic
def copy(D):
    """Returns a dictionary with a copy of all (key, value) pairs in `D`."""

    return {k: v for (k, v) in items(D)}


#
# Views
#
class View(object):
    def __new__(cls, obj):
        new = object.__new__(cls)
        new._delegate = obj
        return new

    def __str__(self):
        data = ', '.join(map(str, iter(self)))
        return '%s(%s)' % (type(self._delegate).__name__, data)


@is_generic
class items(View):
    """
    A set-like object providing a view on a mapping's items

    Examples:
        >>> ('foo', 'bar') in items({'foo': 'bar', 'ham': 'spam'})
        True
    """

    def __contains__(self, item):
        key = item[0]
        return (key, self._delegate[key]) == item

    def __iter__(self):
        D = self._delegate
        for k in D:
            yield (k, D[k])


@is_generic
class values(View):
    """
    A set-like object providing a view on a mapping's values

    Examples:
        >>> 'bar' in values({'foo': 'bar', 'ham': 'spam'})
        True
    """

    def __contains__(self, value):
        D = self._delegate
        for k in D:
            if D[k] == value:
                return True
        else:
            return False

    def __iter__(self):
        D = self._delegate
        for k in D:
            yield D[k]


class keys(View):
    """A set-like object providing a view on a mapping's keys

    Examples:
        >>> 'foo' in keys({'foo': 'bar', 'ham': 'spam'})
        True
    """

    def __contains__(self, key):
        return contains(self._delegate, key)

    def __iter__(self):
        return iter(self._delegate)

