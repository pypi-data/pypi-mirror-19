from pyfunk.monads import maybe
from pyfunk.monads.maybe import Maybe
from pyfunk.misc import F


def test_of():
    assert isinstance(Maybe.of(3), Maybe)
    assert Maybe.of(3)._value == 3


def test_nothing():
    assert Maybe.of(None).nothing()
    assert Maybe.of(None)._value is None


def test_fmap():
    assert Maybe.of(4).fmap(lambda x: x * 2)._value == 8
    assert Maybe.of(None).fmap(lambda x: x * 2).nothing()


def test_join():
    assert Maybe.of(4).fmap(lambda x: Maybe.of(x * 2)).join()._value == 8


def test_chain():
    assert Maybe.of(3).chain(lambda x: Maybe.of(x * 2))._value == 6


def test_or_else():
    assert maybe.or_else(3, Maybe.of(4)) == 4
    assert maybe.or_else(3, Maybe.of(None)) == 3


def test_maybify():
    fn = maybe.maybify(F)(lambda x: None if x > 2 else x)
    assert isinstance(fn(1), Maybe)
    assert fn(12).nothing()


def error():
    raise Exception()


def test_ftry():
    assert maybe.ftry(error)().fmap(lambda x: x * 3).nothing()
    assert maybe.ftry(lambda: 3)().fmap(lambda x: x * 3)._value == 9


def test_cata():
    assert maybe.cata(lambda: "No", lambda x: x * 2, Maybe.of(2)) == 4
    assert maybe.cata(lambda: "No", lambda x: x * 2, Maybe.of(None)) == "No"
