from pyfunk import combinators as comb
from pyfunk.monads import Monad


def ftry(fn):
    """
    Equivalent to try-except using Either monad
    @sig ftry :: Either e => (* -> a) -> (* -> e b a)
    """
    def trier(*args, **kwargs):
        try:
            return Right.of(fn(*args, **kwargs))
        except Exception as e:
            return Left.of(e)
    return trier


@comb.curry
def cata(f, g, e):
    """
    Extracts the values from either for transformation using f is for
    Left and g for Right
    @sig cata :: Either e => (a -> c) -> (b -> d) -> e a b -> d
    """
    if isinstance(e, Left):
        return f(e._value)
    elif isinstance(e, Right):
        return g(e._value)


class Left(Monad):

    def fmap(self, fn):
        """
        Does nothing
        @sig fmap :: Left l => (a -> b) -> l a
        """
        return self

    def join(self):
        """
        Returns the same left monad
        @sig join :: Left l => _ -> l a
        """
        return self


class Right(Monad):
    pass
