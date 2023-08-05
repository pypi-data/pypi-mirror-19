from functools import reduce, wraps


def curry(f):
    '''
    Returns the curried equivalent of the given function.
    @sig curry :: * -> b -> * -> b
    '''
    @wraps(f)
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) == f.__code__.co_argcount:
            return f(*args, **kwargs)
        return lambda *args2, **kwargs2: curried(*(args + args2), **dict(kwargs, **kwargs2))
    return curried


def compose(*fns):
    '''
    Performs right-to-left function composition. The rightmost function may have
    any arity, the remaining functions must be unary.
    @sig compose :: (b -> c)...(* -> b) -> (* -> c)
    '''
    return reduce(lambda f, g:
                  lambda *args: f(g(*args)), fns)


def fnot(f):
    '''
    Creates a function that negates the result of the predicate.
    @sig fnot :: (* -> Bool) -> * -> Bool
    '''
    return lambda *args: not f(*args)


def K(a):
    '''
    The K combinator
    @sig K :: a -> (* -> a)
    '''
    return lambda *args, **kwargs: a


def Y(f):
    return (lambda x:
            f(lambda *args:
              (x(x))(*args)))(
                  lambda x:
                  f(lambda *args:
                    (x(x))(*args)))
