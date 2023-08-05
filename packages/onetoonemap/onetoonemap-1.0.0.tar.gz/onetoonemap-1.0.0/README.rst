===========
onetoonemap
===========

This is a python module that implements a 1:1 mapping type - similar to a ``dict``, but as well as looking up values by keys (``m[k] -> v``), you can look up keys by values (``m[v] -> k``). 

Given ``m = OneToOneMap()``, the following constraints are always true:

.. code:: python

    m.get(key) == value
    m.get(value) == key

    m.keys() == set(m.keys())
    m.values() == set(m.values())
    set(m.keys()) & set(m.values()) == set()
    set.(m.keys()).isdisjoint(set(m.values())) == True


