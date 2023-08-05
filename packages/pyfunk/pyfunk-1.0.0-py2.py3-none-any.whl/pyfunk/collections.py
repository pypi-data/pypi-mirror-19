"""
This is a bunch of Maybe friendly functions for dealing with lists
(lists and tuples) and dictionaries. In other words it's a group of
None-naive functions for dealing with collections
"""

import functools as func

from pyfunk import combinators as comb


@comb.curry
def in_range_p(coll, x):
    """
    Ensures the given index is in the range of the collection
    @sig in_range_p :: [a] -> int -> bool
    """
    return 0 <= x < len(coll)


""" Compliment of in_rangep """
in_range_pc = comb.fnot(in_range_p)


def iterable_p(coll):
    """
    Confirms if a collection is iterable
    @sig iterable_p :: [a] -> bool
    """
    return hasattr(coll, '__len__')


""" Compliment of iterablep """
iterablepc = comb.fnot(iterable_p)


def is_list(coll):
    """
    Returns true if the collection is a list or a tuple.
    @sig is_list :: [a] -> bool
    """
    return isinstance(coll, list) or isinstance(coll, tuple)


def is_pure_list(coll):
    """
    Returns true if and only if the collection is a list.
    @sig is_pure_list :: [a] -> bool
    """
    return isinstance(coll, list)


def is_dict(coll):
    """
    Returns true if the collection passed is a dictionary.
    @sig is_dict :: [a] -> bool
    """
    return isinstance(coll, dict)


def seq(coll):
    """
    Converts a map into a list of key-value pairs. If the given
    collection is a list it simply returns it.
    @sig seq :: [a] -> #(a)
    """
    if is_dict(coll):
        return coll.items()
    return coll


def keys(coll):
    """
    Returns all the keys of a collection
    @sig keys :: [a] -> #(int | str)
    """
    if is_dict(coll):
        return coll.keys()
    elif is_list(coll):
        return range(len(coll))


def items(coll):
    """
    Returns a list of key-value pairs of the collection
    @sig items :: [a] -> #((int | str, a))
    """
    return ((k, coll[k]) for k in keys(coll))


@comb.curry
def conj(coll, x):
    """
    Conjoins a new element to a collection
    @sig conj :: [a] -> a -> [a]
    """
    if is_dict(coll):
        if iterablepc(x) or len(x) != 2:
            raise ValueError("Expected two-element tuple/list got %d" %
                             len(x))
        coll[x[0]] = x[1]
    elif is_list(coll):
        coll.append(x)
    else:
        raise TypeError('Expected a mutable collection type but got %s' %
                        type(coll))
    return coll


@comb.curry
def into(tocoll, fromcoll):
    """
    Reduces the elements of `fromcoll` into `tocoll`
    @sig into :: [a] -> [a] -> [a]
    """
    return func.reduce(conj, seq(fromcoll), tocoll)


@comb.curry
def fmap(fn, coll):
    """
    Curried version of python's map.
    @sig fmap :: (a -> b) -> [a] -> [b]
    """
    return map(fn, seq(coll))


@comb.curry
def fslice(x, y, coll):
    """
    Composable equivalent of [:]. Use None when you don't want to
    pass a value.
    @sig fslice :: int -> int -> [a] -> [a]
    """
    return coll[x:y]


@comb.curry
def freduce(fn, init, coll):
    """
    Composable equivalent of reduce in functional tools. Pass None
    if no init exists.
    @sig freduce :: a -> (a -> b) -> [a] -> b
    """
    coll = seq(coll)
    return func.reduce(fn, coll, init) if init is not None \
        else func.reduce(fn, coll)


@comb.curry
def ffilter(fn, coll):
    """
    Curried version of python's filter.
    @sig fmap :: (a -> bool) -> [a] -> [a]
    """
    return filter(fn, seq(coll))


@comb.curry
def prop(coll, i):
    """
    Property access as a function and None if the key does not exist
    @sig prop :: [a] -> int | str -> a
    """
    if is_dict(coll):
        return coll.get(i, None)
    elif is_list(coll):
        return coll[i] if in_range_p(coll, i) else None


def first(coll):
    """
    You all know Haskell's and lisp's first. If you don't
    it is the first element in the list
    @sig first :: [a] -> a
    """
    return prop(coll, 0)


def rest(coll):
    """
    Anti-first :). Basically everything except the first.
    @sig rest :: [a] -> [a]
    """
    return fslice(1, None, coll)


@comb.curry
def prop_in(coll, keys):
    """
    Performs a tree like depth traversal on the collection using
    the `keys` passed to it.
    @sig prop_in :: [a] -> [str | int] -> a
    """
    n, ots = first(keys), rest(keys)
    # we are at a leaf
    if n is None:
        return coll

    # next node
    v = prop(coll, n)
    return v if v is None else prop_in(v, ots)


@comb.curry
def assoc(coll, k, v):
    """
    Use this to set the value of an item in a collection. Behaves like
    insert with lists when the index goes beyond the size
    @sig assoc :: [a] -> str | int -> a -> [a]
    """
    try:
        coll[k] = v
    except IndexError:
        coll.insert(k, v)
    return coll


@comb.curry
def assoc_in(coll, keys, v):
    """
    Performs a tree like depth write to the collection based on the given
    `keys`. This function unlike the others creates a map if a nested key
    does not exist.
    @sig assoc_in :: [a] -> [str | int] -> a -> [a]
    """
    coll = {} if coll is None else coll
    n, ots = first(keys), rest(keys)

    if len(ots) == 0:
        return assoc(coll, n, v)

    coll = assoc(coll, n, assoc_in(prop(coll, n), ots, v))
    return coll


def usable(coll):
    """
    Most of the functions above that are supposed to return a list return
    some lazy version, use this function to enable external use. It returns
    a sorted list
    @sig usable :: #(a) -> [a]
    """
    return sorted(list(coll))
