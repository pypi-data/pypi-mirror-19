import functools
import pyfunk.combinators as comb
from pyfunk.monads import Monad


@comb.curry
def or_else(x, mb):
    """
    Extract a Maybe's value providing a default if Nothing
    @sig or_else :: b -> Maybe a -> b
    """
    return x if mb.nothing() else mb._value


@comb.curry
def ftry(fn):
    """
    Wraps the result of a try/except operation in a Maybe.
    @sig cata :: Maybe m => (* -> a) -> (* -> m a)
    """
    @functools.wraps(fn)
    def safe(*args, **kwargs):
        try:
            return Maybe.of(fn(*args, **kwargs))
        except:
            return Maybe.of(None)
    return safe


@comb.curry
def cata(f, g, mb):
    """
    Calls f if nothing exists and g if one does.
    @sig cata :: Maybe e => (_ -> _) -> (a -> b) -> m a -> b
    """
    return f() if mb.nothing() else g(mb._value)


@comb.curry
def maybify(nullify, f):
    """
    Creates a function that returns Maybe. Also accepts a Nonifier
    that checks that transforms falsy value to None. One can use
    misc.F if there is no need to nonify.
    @sig maybify :: (a -> Bool) -> (a -> b) -> (a -> Maybe b)
    """
    return comb.compose(lambda a: Maybe.of(None if nullify(a) else a), f)


class Maybe(Monad):

    def nothing(self):
        """
        Checks if the value of this Maybe is None.
        @sig nothing :: Maybe m => _ -> Bool
        """
        return self._value is None

    def fmap(self, fn):
        """
        Transforms the value of the Maybe monad using the given function
        @sig fmap :: Maybe m => (a -> b) -> Maybe b
        """
        return (Maybe.of(None) if self.nothing()
                else Maybe.of(fn(self._value)))

    def join(self):
        """
        Lifts an Maybe monad out of another
        @sig join :: Maybe i => i (i a) -> c a
        """
        return (Maybe.of(None) if self.nothing()
                else self._value)
