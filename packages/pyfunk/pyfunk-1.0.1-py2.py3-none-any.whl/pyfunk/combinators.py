from functools import reduce, wraps


def arg_n(f):
    """
    Returns the number of arguments allowed for the given function `f`
    @sig arg_n :: (* -> a) -> int
    """
    return f.__code__.co_argcount


def multi_args(f):
    """
    Creates a function that only takes the first n arguments passed to
    it, where n is the number of arguments in f
    @sig multi_args :: (* -> a) -> (* -> a)
    """
    return wraps(f)(lambda *args: f(args[:arg_n(f)]))


def curry(f):
    """
    Returns the curried equivalent of the given function. It does not work
    with keyword arguments.
    @sig curry :: * -> b -> * -> b
    """
    @wraps(f)
    def curried(*args):
        if len(args) == arg_n(f):
            return f(*args)
        return lambda *args2: curried(*(args + args2))
    return curried


def compose(*fns):
    """
    Performs right-to-left function composition. The rightmost function may
    have any arity, the remaining functions must be unary.
    @sig compose :: (b -> c)...(* -> b) -> (* -> c)
    """
    return reduce(lambda f, g:
                  lambda *args: f(g(*args)), fns)


def compose_v(*fns):
    """
    Performs right-to-left function composition. Unlike compose though it gives
    the other functions access to the other arguments in the order they were
    passed to the first function, passing the result of the previous function
    as the first argument.
    @sig compose_v :: (* -> c)...(* -> b) -> (* -> c)
    """
    # needs to work like compose
    fns = list(reversed(fns))

    def composition(*args):
        # get first argument for first function
        res = args[0]

        for f in fns:
            # first arg is data from last computation
            fargs = (res,) + args[1:arg_n(f)]
            res = f(*fargs)
        return res
    return composition


def fnot(f):
    """
    Creates a function that negates the result of the predicate.
    @sig fnot :: (* -> Bool) -> * -> Bool
    """
    return lambda *args: not f(*args)


def K(a):
    """
    The K combinator
    @sig K :: a -> (* -> a)
    """
    return lambda *args, **kwargs: a


def Y(f):
    """
    You don't want to know what it is. But it turns a recursive function
    to a non-recursive one.
    @sig Y :: ((* -> a) -> (* -> a)) -> (* -> a)
    """
    return (lambda x:
            f(lambda *args:
              (x(x))(*args)))(
                  lambda x:
                  f(lambda *args:
                    (x(x))(*args)))
