from maputil.api import copy
from sequtil import repeated

#
# Queries
#
_any = any
_default = object()


def isinstance_keys(map, type, any=False):
    """
    Return True if all keys are instances of a given type or tuple of types.

    If ``any=True``, return True if any of the keys are instances of the given
    class.

    Example:
        >>> isinstance_keys({1: 'one', 2: 'two'}, int)
        True
        >>> isinstance_keys({1: 'one', 2: 'two', 3.14: 'pi'}, int)
        False
        >>> isinstance_keys({1: 'one', 2: 'two', 3.14: 'pi'}, int, any=True)
        True

    See also:
        isinstance_values() -- similar, but works with dictionary values
        isinstance_items()  -- similar, but works with dictionary
                               (key, value) pairs
    """
    ev = _any if any else all
    return ev(isinstance(k, type) for k in map)


def isinstance_values(map, type, any=False):
    """
    Return True if all values are instances of a given type or tuple of types.

    If ``any=True``, return True if any of the values are instances of the
    given class.

    Example:
        >>> isinstance_values({1: 'one', 2: 'two'}, str)
        True
        >>> isinstance_values({'one': 1, 'pi': 3.14}, float, any=True)
        True

    See also:
        isinstance_keys()   -- similar, but works with dictionary keys
        isinstance_items()  -- similar, but works with dictionary (key, value)
                               pairs
    """

    ev = _any if any else all
    return ev(isinstance(v, type) for v in map.values())


def isinstance_items(map, type_keys, type_values, any=False):
    """
    Return True if all values are instances of the given types.

    If ``any=True``, return True if any of the (key, value) pairs are instances
    of the given classes.

    Example:
        >>> isinstance_items({1: 'one', 2: 'two'}, int, str)
        True
        >>> isinstance_items({'one': 1, 'pi': 3.14}, str, float, any=True)
        True

    See also:
        isinstance_keys() -- similar, but works with dictionary keys
        isinstance_values()  -- similar, but works with dictionary values
    """

    ev = _any if any else all
    return ev(
        isinstance(k, type_keys) and isinstance(v, type_values)
        for (k, v) in map.items()
    )


def is_bijection(map):
    """
    Return True if mapping is a bijection and False otherwise

    Example:
        >>> is_bijection({1: 2, 3: 5})
        True

        >>> is_bijection({1: 2, 3: 2})
        False
    """

    # Try fast implementation that depends on items being hashable
    try:
        unique = set(map.values())
    except TypeError:
        pass
    else:
        return len(unique) == len(map)

    # Implementation that works with non-hashable types
    unique = []
    for v in map.values():
        if v in unique:
            return False
        unique.append(v)
    return True


#
# Representation and printing ???
#
def _srepr(map):
    pass


def _sprint(map):
    pass


#
# Other utility functions
#
def getkey(map, value, default=_default):
    """
    Return one key that maps to the given value.

    If more than one key maps to the given value, the result will be
    unpredictable.

    Raises a KeyError if no key is found. An optional default value can be
    given as a third positional argument instead, and is returned if no key
    is found.

    Example:
        >>> getkey({1: 'one', 2: 'two'}, 'one')
        1
        >>> getkey({1: 'one', 2: 'two'}, 'three', None)
        None
    """

    for k, v in map.items():
        if v == value:
            return k
    else:
        if default is _default:
            raise KeyError('no keys points to %r' % value)
        else:
            return default


def getkey_unique(map, value, default=_default):
    """
    Similar to getkey(), but raises a ValueError if the key is not unique

    Example:
        >>> getkey_unique({1: 'one', 2: 'two'}, 'one')
        1
        >>> getkey_unique({3.14: 'pi', 2: 'two', 3.1415: 'pi'}, 'pi')
        Traceback (most recent call last):
        ...
        ValueError: repeated keys: 3.1415, 3.14
    """

    out = _default
    items = iter(map.items())

    # Find the associated key
    for k, v in items:
        if v == value:
            out = k
            break
    else:
        if default is _default:
            raise KeyError('no keys points to %r' % value)
        else:
            return default

    # Checks if the key is unique
    for k, v in items:
        if v == value:
            raise ValueError('repeated keys: %r, %r' % (out, k))
    return out


def _getkeys(map, keys):
    return NotImplemented


def ichangekey(map, old, new, replace=False):
    """
    Change the name of the given key *inplace*.

    Raises a ValueError if the new key is present in the dictionary, unless
    ``replace=True``, in which the existing key is replaced.

    Example:
        >>> D = {1.0: 'one'}
        >>> ichangekey(D, 1.0, 1); D
        {1: 'one'}
    """
    if replace:
        value = map.pop(old)
        map[new] = value
    else:
        type_new = type(new)
        type_old = type(old)
        if new in map and not (new == old and type_new is type_old):
            raise ValueError('%r already present in dictionary' % new)
        value = map.pop(old)
        map[new] = value


def ichangekeys(map, keymap, replace=False):
    """Like :func:`changekeys`, but make changes *inplace*."""

    return NotImplemented


def changekeys(map, keymap, replace=False):
    """
    Return a copy of map with the name of the keys changed according to the
    given keymap.

    Example:
        >>> changekeys({1: 2, 3: 4}, {1: 3, 3: 1})
        {3: 2, 1: 4}
    """

    return NotImplemented


def count(map, *args):
    """
    Count the number of occurrences of the given value.

    If the second argument is not given, return a list with the counts of all
    values.
    """

    return NotImplemented


def inv(map, raises=True):
    """
    Invert the (key, value) relation.

    If ``raises=True`` (default), raises a ValueError if duplicate values are
    found. Otherwise, it picks up a mapping randomly.

    Example:
        >>> D = {1: 2, 3: 4}
        >>> inv(D) == {2: 1, 4: 3}
        True

        It automatically detects repeated values

        >>> D = {1: 2, 3: 2}
        >>> inv(D)
        Traceback (most recent call last):
        ...
        ValueError: repeated values: [2]
    """

    inv = {v: k for (k, v) in map.items()}

    # Detect broken bijections and raise errors
    if raises and len(inv) != len(map):
        raise ValueError('repeated values: %s' % repeated(list(map.values())))
    return inv


def unique_values(map, inplace=False):
    """Returns a dictionary with the subset of (key, value) mappings in which
    values are unique.

    Example:
        >>> D = {1: 2, 2: 3, 3: 2}

        Remove (1, 2) and (3, 2) since both items point to the same value,
        breaking the bijection

        >>> unique_values(D)
        {2: 3}

    See also:
        assure_bijection() -- raises a ValueError if a map is not a bijection
        is_bijection() -- query if a dictionary is bijective
        repeated_values() -- does the complementary operation
    """

    if inplace:
        out = map
    else:
        out = copy(map)

    # Create a list of duplicate values
    values = list(map.values())
    for v in set(values):
        values.remove(v)

    # Del all items in the duplicate values list
    for k, v in list(out.items()):
        if v in values:
            del out[k]

    # Return if computation is not inplace
    if not inplace:
        return out


def repeated_values(map, inplace=False):
    """Returns a dictionary with the subset of (key, value) mappings in which
    values are repeated. Concatenating the result of ``unique_values(D)`` and
    ``repeated_values(D)`` restores the dictionary.


    Example
    -------

    >>> D = {1: 2, 2: 3, 3: 2}

    Keeps only (1, 2) and (3, 2) since both items point to the same value.

    >>> repeated_values(D)
    {1: 2, 3: 2}

    See also
    --------

    assure_bijection() -- raises a ValueError if a dictionary is not bijective
    is_bijection() -- query if a dictionary is bijective
    unique_values() -- does the complementary operation
    """

    if inplace:
        out = map
    else:
        out = copy(map)

    # Create a list of duplicate values
    values = list(map.values())
    for v in set(values):
        values.remove(v)

    # Del all items in the duplicate values list
    for k, v in list(out.items()):
        if v not in values:
            del out[k]

    # Return if computation is not inplace
    if not inplace:
        return out


def inv_merge(map, collection=None):
    """
    Invert the dictionary by merging (key, value) pairs with the same values
    into ``value: {key1, key2, ...}`` mappings in the output. Non-repeated
    values are mapped to a single element set.


    Example:
        >>> D = {1: 2, 2: 3, 3: 2}
        >>> inv_merge(D) == {2: {1, 3}, 3: {2}}
        True
    """
    out = {}
    for k, v in map.items():
        if v in out:
            out[v].add(k)
        else:
            out[v] = {k}

    if collection is not None:
        for k, v in out.items():
            out[k] = collection(v)

    return out


#
# Key selection
#
def select_keys(map, keys, default=_default):
    """
    Return a dictionary with the given keys selected from map.

    User can provide an optional default value for non-existing keys. Otherwise
    a KeyError is raised.

    Example:
        >>> D = select_keys({1: 2, 3: 4, 5: 6}, [1, 2, 3], None)
        >>> D == {1: 2, 2: None, 3: 4}
        True
    """

    if default is _default:
        return {k: map[k] for k in keys}
    else:
        return {k: map.get(k, default) for k in keys}


def unselect_keys(map, keys):
    """
    Return a new dictionary from map discarding any key from the given keys
    list.

    Example:
        >>> unselect_keys({1: 2, 3: 4, 5: 6}, [1, 2, 3])
        {5: 6}
    """
    try:
        keys = set(keys)
    except TypeError:
        keys = list(keys)

    out = {}
    for k, v in map.items():
        if k not in keys:
            out[k] = v
    return out
