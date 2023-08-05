#!/usr/bin/env python2.7
"""
A python module that implements a 1:1 mapping collection type
"""

from collections import MutableMapping

class OneToOneMap(MutableMapping):
    """
    1:1 mapping type. Objects of this type can be treated like a dict,
    except that keys and values can both be used to look each other up.
    This also implies that all keys are unique, all values are unique,
    and there is no overlap between keys and values:

    m = OneToOneMap()

    m.get(key) == value
    m.get(value) == key

    m.keys() == set(m.keys())
    m.values() == set(m.values())
    set(m.keys()) & set(m.values()) == set()
    set.(m.keys()).isdisjoint(set(m.values())) == True
    """

    def __init__(self, *args, **kwargs):
        self.__keymap = {}
        self.__valmap = {}
        self.update(*args, **kwargs)

    def __str__(self):
        return str(self.__keymap)

    def __repr__(self):
        return repr(self.__keymap)

    def __setitem__(self, k, v):
        # Overwriting a key/value with itself is allowed but a no-op
        if k in self.__keymap and self.__keymap[k] == v:
            return

        # Values must be unique
        if v in self.__valmap:
            raise ValueError("Value must be unique")
        if v in self.__keymap:
            raise ValueError("Value cannot be the same as any key")
        self.__keymap[k] = v
        self.__valmap[v] = k

    def __getitem__(self, k):
        if k in self.__valmap:
            return self.__valmap[k]
        return self.__keymap[k]

    def get(self, k, default=None):
        return self.__keymap.get(k, self.__valmap.get(k, default))

    def __delitem__(self, k):
        v = self.__keymap[k]
        del self.__keymap[k]
        del self.__valmap[v]

    def __iter__(self):
        return iter(self.__keymap)

    def __len__(self):
        return len(self.__keymap)

    def __contains__(self, k):
        return k in self.__keymap or k in self.__valmap

    def __getattr__(self, k):
        if k in self:
            return self[k]
        return MutableMapping.__getattribute__(self, k)

    def clear(self):
        self.__keymap.clear()
        self.__valmap.clear()

    def items(self):
        return self.__keymap.items()

    def keys(self):
        return self.__keymap.keys()

    def values(self):
        return self.__keymap.values()

    def update(self, *args, **kwargs):
        dd = dict(*args, **kwargs)
        keys = dd.keys()
        values = dd.values()

        # All values must be unique
        if any([values.count(item) > 1 for item in values]):
            raise ValueError("All values must be unique")

        # No values can have the same value as any key
        if any([keys.count(item) > 0 for item in values]):
            raise ValueError("No value can be the same as any key")

        self.__keymap.update(dd)
        self.__valmap = {v: k for k, v in self.__keymap.iteritems()}

