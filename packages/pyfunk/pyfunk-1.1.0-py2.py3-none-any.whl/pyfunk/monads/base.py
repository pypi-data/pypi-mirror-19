from pyfunk import combinators as comb


class Monad(object):

    def __init__(self, val):
        self._value = val

    @classmethod
    def of(cls, val):
        """
        Creates a new applicative
        @sig of :: Applicative a => x -> a x
        """
        return cls(val)

    def fmap(self, fn):
        """
        Transforms the value of the functor using the given function
        @sig fmap :: Functor f => (a -> b) -> f b
        """
        return self.of(fn(self._value))

    def join(self):
        """
        Lifts a functor out of another
        @sig join :: Functor f => f (f a) -> f a
        """
        return self._value

    def chain(self, fn):
        """
        Applies a function that produces a chain to the value in this
        chain
        @sig chain :: Chain c => (a -> c b) -> c b
        """
        return self.fmap(fn).join()

    def ap(self, f):
        """
        Applies the function in the Apply on the given functor's
        value. This function must be curried
        @sig ap :: (Apply a,Functor f) => f x -> a y
        """
        return f.fmap(self._value)

    @comb.curry
    def liftA2(self, f1, f2):
        """
        Applies the function in the apply to 2 functors
        @sig ap :: (Apply a,Functor f) => f x -> f y -> a z
        """
        return f1.fmap(self._value).ap(f2)

    @comb.curry
    def liftA3(self, f1, f2, f3):
        """
        Applies the function in the apply to 2 functors
        @sig ap :: (Apply a,Functor f) => f x -> f x -> f y -> a z
        """
        return f1.fmap(self._value).ap(f2).ap(f3)
