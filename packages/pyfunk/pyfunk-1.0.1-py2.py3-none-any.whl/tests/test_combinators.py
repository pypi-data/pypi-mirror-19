import pyfunk.combinators as _
from pyfunk.misc import T


def test_compose():
    fn2 = _.compose(lambda x: x * 4, lambda x: x * 2)
    assert fn2(3) == (3 * 2 * 4)

    fn3 = _.compose(lambda x: x * 8, lambda x: x * 4, lambda x: x * 2)
    assert fn3(3) == (3 * 2 * 4 * 8)


def test_compose_v():
    fn2 = _.compose_v(lambda x, y: x + y, lambda x: x * 2)
    assert fn2(2, 3) == 7

    fn3 = _.compose_v(lambda x, y, z: x + y + z, lambda x: x * x,
                      lambda x, y: x / y)
    assert fn3(6, 2, 2) == 13


def test_curry():
    add3 = _.curry(lambda a, b, c: a + b + c)
    assert add3(1, 2, 3) == 6
    assert add3(1, 2)(3) == 6
    assert add3(1)(2, 3) == 6
    assert add3(1)(2)(3) == 6


def test_fnot():
    twist = _.fnot(T)
    assert twist() is False
    assert twist(1, 2, 3) is False
