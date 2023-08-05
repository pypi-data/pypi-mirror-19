from pyfunk.monads import (
    fmap, chain,
    chaincompose, ap, liftA2,
    liftA3, Monad
)
from pyfunk.combinators import compose, curry


@curry
def add(x, y):
    return x + y


@curry
def add3(x, y, z):
    return x + y + z


def test_fmap():
    x = compose(fmap(lambda x: x * 2), Monad.of)
    assert x(4)._value == 8


def test_chain():
    x = compose(chain(lambda x: Monad.of(x * 2)), Monad.of)
    assert x(4)._value == 8


def test_chaincompose():
    x = chaincompose(lambda x: Monad.of(x * 2), Monad.of)
    assert x(4)._value == 8


def test_ap():
    x = compose(ap(Monad.of, lambda x: x * 2), Monad.of)
    assert x(8)._value == 16


def test_liftA2():
    assert liftA2(add, Monad.of(4), Monad.of(6))._value == 10


def test_liftA3():
    assert liftA3(add3, Monad.of(4), Monad.of(4), Monad.of(4))._value == 12
