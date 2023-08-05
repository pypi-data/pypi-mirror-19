from pyfunk.monads import Monad


class Reader(Monad):

    def __init__(self, fn):
        self.run = fn
