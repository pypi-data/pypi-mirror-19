from pyfunk import combinators as _
from pyfunk.monads import helpers
from pyfunk.monads import Monad


@_.curry
def add(x, y):
    return x + y


@_.curry
def add3(x, y, z):
    return x + y + z


def test_fmap():
    x = _.compose(helpers.fmap(lambda x: x * 2), Monad.of)
    assert x(4)._value == 8


def test_chain():
    x = _.compose(helpers.chain(lambda x: Monad.of(x * 2)), Monad.of)
    assert x(4)._value == 8


def test_chaincompose():
    x = helpers.chaincompose(lambda x: Monad.of(x * 2), Monad.of)
    assert x(4)._value == 8


def test_ap():
    x = _.compose(helpers.ap(Monad.of, lambda x: x * 2), Monad.of)
    assert x(8)._value == 16


def test_liftA2():
    assert helpers.liftA2(add, Monad.of(4), Monad.of(6))._value == 10


def test_liftA3():
    assert helpers.liftA3(add3, Monad.of(4),
                          Monad.of(4), Monad.of(4))._value == 12
