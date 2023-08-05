from pyfunk.misc import fid, T, F


def test_fid():
    assert fid(3) == 3


def test_T():
    assert T() is True


def test_F():
    assert F() is False
