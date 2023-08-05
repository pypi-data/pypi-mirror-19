import collections
from sequtil.api_generics import copy_docstrings

__all__ = ['Mapping']


@copy_docstrings(dict)
class Mapping(object):
    """
    A Mapping base class that can be used to implement generic mappings
    by supplying the methods ``__getitem__``, ``__iter__``, ``__len__`` (for
    immutable types), ``__delitem__``, and ``__setitem__`` (for mutable types).

    The implementation is borrowed from collections.MutableMapping and it is
    equivalent in most circumstances. ``Mapping`` however does not use abstract
    classes. This allows arbitrary meta-classes being used on the derived types.
    """

    def __delitem__(self, key):
        msg = "'%s' instance does not support deletion" % type(self).__name__
        raise ValueError(msg)

    def __getitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __setitem__(self, key, value):
        msg = "'%s' instance does not support mutation" % type(self).__name__
        raise AttributeError(msg)

    def __repr__(self):
        try:
            name = type(self).__name__
            data = ', '.join(
                '%s: %s' %
                (repr(k),
                 repr(v)) for (
                    k,
                    v) in self.items())
            return '%s(%s)' % (name, data)
        except NotImplementedError:
            return object.__repr__(self)

    __DEFAULT = object()

    def pop(self, key, default=__DEFAULT):
        try:
            value = self[key]
        except KeyError:
            if default is self.__DEFAULT:
                raise
            return default
        else:
            del self[key]
            return value

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for k, v in self.items():
            try:
                if other[k] != v:
                    return False
            except KeyError:
                return False
        return True

#    def viewkeys(self):
#        return viewkeys(self)
#
#    def viewvalues(self):
#        return viewvalues(self)
#
#    def viewitems(self):
#        return viewitems(self)

for name in dir(collections.MutableMapping):
    if (name.startswith('_') and not name.startswith('__')
            or name in ('__module__', '__metaclass__')):
        continue
    if not hasattr(Mapping, name):
        method = getattr(collections.MutableMapping, name)
        if callable(method):
            method = getattr(method, 'im_func', None) or method
            setattr(Mapping, name, method)
del name, method
