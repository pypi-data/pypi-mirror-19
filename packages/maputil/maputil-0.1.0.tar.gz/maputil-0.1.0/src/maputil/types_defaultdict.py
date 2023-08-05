import itertools
from dicttools.types_base import Mapping
from dicttools.api_generics import copy_docstrings

__all__ = ['defaultdict']


@copy_docstrings(dict)
class defaultdict(Mapping, dict):

    def __init__(self, default, *args, **kwds):
        '''
        Dictionary that acts as a diff from a default dictionary.

        default : dict
            Dictionary with the default values.

        Special attributes
        ------------------

        `defaultdict` has a similar API to ordinary dictionaries. It also
        defines a few extra attributes:

        default : dict
            The default dictionary.
        local : dict
            A copy of all data that differs from the default dictionary.
        flat : dict
            A flattened version of itself, i.e., a regular dictionary which
            contains all (key, value) pairs of the `defaultdict` instance.

        Usage
        -----

        This class acts as an independent dictionary that only stores the
        differences from a default dictionary. The ``defaultdict`` instance can
        create new keys or modify existing values.

        >>> default = {'foo': 'bar', 'ham': 'spam'}
        >>> D = defaultdict(default, ham='eggs')
        >>> D == {'foo': 'bar', 'ham': 'eggs'}
        True

        You can add new attributes to D

        >>> D['foobar'] = None
        >>> D == {'foo': 'bar', 'ham': 'eggs', 'foobar': None}
        True

        Only the ones that differ from `default` are stored

        >>> D.default == {'foo': 'bar', 'ham': 'spam'}
        True
        >>> D.local == {'foobar': None, 'ham': 'eggs'}
        True

        Observation
        -----------

        Changes to the default dictionary are propagated. Consider the the
        example:

        >>> default = {'foo': 'bar'}
        >>> D = defaultdict(default, ham='spam')
        >>> D ==  {'foo': 'bar', 'ham': 'spam'}
        True

        Changing the default also changes D. It is generaly safe to change the values of the
        default dictionary. Adding/deleting keys in the middle of an iteration,
        however, can lead to trouble. In those cases it is a good practice to
        use either a `frozendict` or a `frozenkeydict` as default dictionaries.

        >>> default['foo'] = 'foobar' # now 'foo' is mapped to 'foobar'
        >>> D == {'foo': 'foobar', 'ham': 'spam'}
        True
        '''

        self._default = default
        dict.__init__(self, *args, **kwds)

    def absorb(self):
        '''Absorb all keys in the default dictionary in the local dictionary.

        Example
        --------

        >>> D = defaultdict({'foo': 'bar'}, ham='spam')
        >>> D.absorb()
        >>> D.local == {'foo': 'bar', 'ham': 'spam'}
        True
        '''

        for k, v in self._default.items():
            dict.setdefault(self, k, v)

    def purge(self):
        '''Remove all keys from the local dictionary that are identical to the
        to the default one.

        Example
        --------

        >>> D = defaultdict({'foo': 'bar'})

        By setting 'foo' to 'bar', this information is stored in the local
        dictionary.

        >>> D['foo'] = 'bar'
        >>> D.local == {'foo': 'bar'}
        True

        D.purge() erases the redundant information.

        >>> D.purge()
        >>> D.local == {}
        True
        '''

        D = self._default
        for (k, v) in list(dict.items(self)):
            if D[k] == v:
                dict.__delitem__(self, k)

    @property
    def default(self):
        return self._default

    @property
    def local(self):
        return dict(dict.items(self))

    @property
    def flat(self):
        return dict(self.iteritems())

    # immutable mapping ABC --------------------------------------------------
    def __getitem__(self, k):
        try:
            return dict.__getitem__(self, k)
        except KeyError:
            return self._default[k]

    def __iter__(self):
        has_local = dict.__contains__
        it_self = dict.__iter__(self)
        it_remain = iter(k for k in self._default if not has_local(self, k))
        return itertools.chain(it_remain, it_self)

    def __len__(self):
        has_local = dict.__contains__
        it_remain = iter(1 for k in self._default if not has_local(self, k))
        return dict.__len__(self) + sum(it_remain)

    # mutable mapping API ----------------------------------------------------
    def __setitem__(self, k, v):
        dict.__setitem__(self, k, v)

    def __delitem__(self, k):
        try:
            dict.__delitem__(self, k)
        except KeyError as ex:
            if k in self._default:
                raise KeyError(
                    'cannot delete key from default dictionary, %s' %
                    repr(k))
            else:
                raise ex

    # magic methods ----------------------------------------------------------
    def __contains__(self, k):
        return dict.__contains__(self, k) or k in self._default

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.flat)

    def __str__(self):
        return repr(self)

    def clear(self):
        '''Clear all local keys from dictionary. It will usually result in a
        non-empty dictionary (unless self.default is empty).'''

        dict.clear(self)

    def copy(self):
        return defaultdict(self._default, **self.local())

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
