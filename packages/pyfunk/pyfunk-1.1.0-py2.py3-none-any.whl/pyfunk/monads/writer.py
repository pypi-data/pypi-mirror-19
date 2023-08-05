from pyfunk.monads import Monad


class Writer(Monad):

    def __init__(self, val, *info):
        super().__init__(val)
        self._info = info

    @classmethod
    def of(cls, val):
        '''
        Unit function for creating writer monad
        @sig of :: Writer w => a -> w a
        '''
        return Writer(val)

    def fmap(self, fn):
        '''
        Transforms the value in the Writer monad producing
        a new value and extra info
        @sig fmap :: Writer w => (a -> (b c)) -> w b
        '''
        val, info = fn(self._value)
        return Writer(val, *(self.info + (info,)))
