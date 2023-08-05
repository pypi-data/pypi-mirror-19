from pyfunk import combinators as comb
from pyfunk.monads import Monad


@comb.curry
def add(x, y):
    return x + y


@comb.curry
def add3(x, y, z):
    return x + y + z


def test_of():
    assert isinstance(Monad.of(3), Monad)
    assert Monad.of(3)._value == 3


def test_fmap():
    assert Monad.of(4).fmap(lambda x: x * 2)._value == 8


def test_join():
    assert Monad.of(4).fmap(lambda x: Monad.of(x * 2)).join()._value == 8


def test_chain():
    assert Monad.of(3).chain(lambda x: Monad.of(x * 2))._value == 6


def test_ap():
    assert Monad.of(add).ap(Monad.of(4)).ap(Monad.of(8))._value == 12


def test_liftA2():
    assert Monad.of(add).liftA2(Monad.of(4), Monad.of(4))._value == 8


def test_liftA3():
    assert Monad.of(add3).liftA3(
        Monad.of(4), Monad.of(4), Monad.of(4))._value == 12
