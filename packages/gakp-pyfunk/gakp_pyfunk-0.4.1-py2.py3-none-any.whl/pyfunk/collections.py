import functools as func
from pyfunk import combinators as comb


def __empty_collection(coll):
    return [] if coll is None else coll


def __map_to_list(coll):
    if isinstance(coll, dict):
        return list(coll.items())
    return coll


def __in_range(coll, x):
    return 0 < x < len(coll)


def keys(coll):
    '''
    Returns all the keys of a collection
    @sig keys :: [a] -> [int | str]
    '''
    coll = __empty_collection(coll)
    if isinstance(coll, dict):
        return list(coll.keys())
    else:
        return list(range(len(coll)))


def items(coll):
    '''
    Returns a list of key-value pairs of the collection
    @sig items :: [a] -> [(int | str, a)]
    '''
    coll = __empty_collection(coll)
    return [(k, coll[k]) for k in keys(coll)]


@comb.curry
def conj(coll, x):
    '''
    Conjoins a new element to a collection
    @sig conj :: [a] -> a -> [a]
    '''
    coll = __empty_collection(coll)
    if isinstance(coll, dict):
        if not(hasattr(x, '__len__')) or len(x) != 2:
            raise ValueError("Expected two-element tuple/list got %d" % len(x))
        coll[x[0]] = x[1]
    else:
        coll.append(x)
    return coll


@comb.curry
def into(tocoll, fromcoll):
    '''
    Reduces the elements of `fromcoll` into `tocoll`
    @sig into :: [] -> [a] -> [a]
    '''
    fromcoll = __map_to_list(__empty_collection(fromcoll))
    return func.reduce(conj, fromcoll, tocoll)


@comb.curry
def fmap(fn, coll):
    '''
    Curried version of python's map.
    @sig fmap :: (a -> b) -> [a] -> [b]
    '''
    coll = __map_to_list(__empty_collection(coll))
    return list(map(fn, coll))


@comb.curry
def fslice(x, y, coll):
    '''
    Composable equivalent of [:]. Use None when you don't want to
    pass a value.
    @sig fslice :: int -> int -> [a] -> [a]
    '''
    coll = __empty_collection(coll)
    return coll[x:y]


@comb.curry
def freduce(init, fn, coll):
    '''
    Composable equivalent of reduce in functional tools. Pass None
    if no init exists.
    @sig freduce :: a -> (a -> b) -> [a] -> b
    '''
    coll = __empty_collection(coll)
    return func.reduce(fn, coll, init) if init else func.reduce(fn, coll)


@comb.curry
def ffilter(fn, coll):
    '''
    Curried version of python's filter.
    @sig fmap :: (a -> bool) -> [a] -> [a]
    '''
    coll = __map_to_list(__empty_collection(coll))
    return list(filter(fn, coll))


@comb.curry
def prop(i, coll):
    '''
    Property access as a function and None if the key does not exist
    @sig prop :: int | str -> [a] -> a
    '''
    if i is None:
        return None
    coll = __empty_collection(coll)
    if isinstance(coll, dict):
        return coll.get(i, None)
    else:
        return coll[i] if __in_range(coll, i) else None


def first(coll):
    '''
    You all know Haskell's and lisp's first. If you don't
    it is the first element in the list
    @sig first :: [a] -> a
    '''
    return prop(0, coll)


def rest(coll):
    '''
    Anti-first :). Basically everything except the first.
    @sig rest :: [a] -> [a]
    '''
    return fslice(1, None, coll)


def prop_in(keys, coll):
    v = prop(first(keys), coll)
    print(v, first(keys))
    return v if v is None else prop_in(rest(keys), v)


@comb.curry
def find_key(fn, coll):
    '''
    Find the key of first element that passes given predicate.
    If not found it returns nothing.
    @sig find_key :: (a -> bool) -> [a] -> int | str
    '''
    for k in keys(coll):
        if fn(prop(k, coll)):
            return k
