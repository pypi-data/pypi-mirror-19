from pyfunk import combinators as comb
from pyfunk.monads import Monad


class IO(Monad):

    def __init__(self, fn):
        """
        Create new IO Monad
        @sig a -> IO a
        """
        self.io = fn

    @classmethod
    def of(cls, x):
        """
        Factory for creating new IO monad
        @sig of :: a -> IO a
        """
        return cls(lambda: x)

    def fmap(self, fn):
        """
        Transforms the value of the IO monad using the given function
        @sig fmap :: IO a => (a -> b) -> IO b
        """
        return IO(comb.compose(fn, self.io))

    def join(self):
        """
        Lifts an IO monad out of another
        @sig join :: IO i => i (i a) -> c a
        """
        return IO(lambda: self.io().io())
