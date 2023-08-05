from pyfunk.monads import Monad


class State(Monad):

    def __init__(self, run):
        self.run = run

    @classmethod
    def of(cls, val):
        return cls(lambda state: (state, val))

    def fmap(self, fn):
        def mapper(state):
            nstate, val = self.run(state)
            return (nstate, fn(val))
        return State(mapper)

    def join(self):
        def joiner(state):
            nstate, smonad = self.run(state)
            return smonad.run(nstate)
        return State(joiner)

    @classmethod
    def get(cls):
        return cls(lambda state: (state, state))

    @classmethod
    def put(cls, nstate):
        return cls(lambda state: (nstate, None))

    @classmethod
    def modify(cls, fn):
        return cls(lambda state: (fn(state), None))

    def execState(self, state):
        return self.run(state)[1]

    def fexec(self, state):
        return self.run(state)[1]
