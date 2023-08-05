from pyfunk.monads.task import Task
from pyfunk.misc import fid


def assertFn(fn):
    def asserter(x):
        assert fn(x)
    return asserter


def test_of():
    assert isinstance(Task.of(3), Task)
    Task.of(3).fork(fid, assertFn(lambda x: x == 3))


def test_rejected():
    assert isinstance(Task.rejected(3), Task)
    Task.rejected(3).fork(assertFn(lambda x: x == 3), fid)


def test_fmap():
    Task.of(4).fmap(lambda x: x * 2).fork(fid, assertFn(lambda x: x == 8))


def test_rejected_fmap():
    Task.rejected(4).rejected_fmap(lambda x: x * 2) \
        .fork(assertFn(lambda x: x == 8), fid)


def test_join():
    Task.of(4).fmap(lambda x: Task.of(x * 2)) \
        .join().fork(fid, assertFn(lambda x: x == 8))


def test_chain():
    Task.of(3).chain(lambda x: Task.of(x * 2)) \
        .fork(fid, assertFn(lambda x: x == 6))


def test_err_chain():
    Task.rejected(3).or_else(lambda x: Task.rejected(x * 2)) \
        .fork(assertFn(lambda x: x == 6), fid)
