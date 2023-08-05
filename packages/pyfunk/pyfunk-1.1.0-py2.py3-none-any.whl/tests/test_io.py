from pyfunk.monads.io import IO


def test_of():
    assert isinstance(IO.of(3), IO)
    assert IO.of(3).io() == 3


def test_fmap():
    io = IO.of(4)
    assert io.fmap(lambda x: x * 2).io() == 8


def test_join():
    assert IO.of(4).fmap(lambda x: IO.of(x * 2)).join().io() == 8


def test_chain():
    assert IO.of(3).chain(lambda x: IO.of(x * 2)).io() == 6
