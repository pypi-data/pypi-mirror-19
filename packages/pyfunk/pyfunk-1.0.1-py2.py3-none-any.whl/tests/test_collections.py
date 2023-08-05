from pyfunk import collections as _
from pyfunk.misc import T


def test_in_range_p():
    assert _.in_range_p([0, 1, 2], 0)
    assert _.in_range_p([0, 1, 2], 2)
    assert not _.in_range_p([0, 1, 2], 3)
    assert not _.in_range_p([0, 1, 2], -1)


def test_iterable_p():
    assert _.iterable_p([])
    assert _.iterable_p((1, 2))
    assert _.iterable_p(dict())
    assert not _.iterable_p(2)


def test_is_list():
    assert _.is_list([])
    assert _.is_list((1, 2))
    assert not _.is_list({1, 2})


def test_is_pure_list():
    assert _.is_pure_list([])
    assert not _.is_pure_list((1, 2))


def test_is_dict():
    assert _.is_dict({})
    assert not _.is_dict([])


def test_into():
    assert _.into({}, dict(a=1, b=2)) == {'a': 1, 'b': 2}
    assert _.into([], [0, 1, 2]) == [0, 1, 2]
    assert _.into({}, [('a', 1), ('b', 2)]) == {'a': 1, 'b': 2}


def test_conj():
    assert _.conj([], 1) == [1]
    assert _.conj({}, ['a', 1]) == {'a': 1}
    assert _.conj({}, ('b', 2)) == {'b': 2}


def test_keys():
    assert _.usable(_.keys([1, 2, 3])) == [0, 1, 2]
    assert _.usable(_.keys({'a': 1, 'b': 2})) == ['a', 'b']


def test_seq():
    assert _.usable(_.seq([1, 2, 3])) == [1, 2, 3]
    assert _.usable(_.seq({'a': 1, 'b': 2})) == [('a', 1), ('b', 2)]


def test_items():
    assert _.usable(_.items({'a': 1, 'b': 2})) == [('a', 1), ('b', 2)]
    assert _.usable(_.items([1, 2])) == [(0, 1), (1, 2)]


def test_fmap():
    oresult = _.into({}, _.fmap(lambda kv:
                                (kv[0], kv[1] * 2),
                                {'a': 1, 'b': 2}))
    assert oresult['a'] == 2
    assert oresult['b'] == 4

    aresult = _.usable(_.fmap(lambda x: x * 2, [1, 2]))
    assert aresult[0] == 2
    assert aresult[1] == 4


def test_fslice():
    aresult = _.fslice(0, 2, [0, 1, 2, 3])
    assert aresult[0] == 0
    assert len(aresult) == 2

    tresult = _.fslice(0, 2, (0, 1, 2, 3))
    assert tresult[0] == 0
    assert len(tresult) == 2

    sresult = _.fslice(0, 5, 'helloworld')
    assert sresult == 'hello'

    allresult = _.fslice(0, None, [0, 1, 2, 3])
    assert len(allresult) == 4


def test_ffilter():
    oresult = _.ffilter(T, {'a': 1, 'b': 2})
    assert len(_.usable(oresult)) == 2

    aresult = _.ffilter(lambda x: x < 3, [0, 1, 2, 3])
    assert len(_.usable(aresult)) == 3


def add_val(o, b):
    k, v = b
    o[k] = v
    return o


def test_freduce():
    assert _.freduce(lambda a, b: a + b, None, [1, 2, 3, 4], 10)
    assert _.freduce(add_val, {}, {'a': 1, 'b': 2}) == {'a': 1, 'b': 2}


def test_prop():
    assert _.prop({'a': 1, 'b': 2}, 'b') == 2
    assert _.prop([4, 1], 0) == 4
    assert _.prop([1, 2], 12) is None


def test_first():
    assert _.first([1, 2, 3, 4, 5]) == 1


def test_rest():
    assert _.rest([1, 2, 3, 4, 5]) == [2, 3, 4, 5]


def test_prop_in():
    assert _.prop_in([[1]], [0, 0]) == 1
    assert _.prop_in({'a': {'b': 1}}, ['a', 'b']) == 1
    assert _.prop_in([], [0, 1]) is None
    assert _.prop_in([[1]], [0, 2]) is None


def test_assoc():
    assert _.assoc([], 0, 1) == [1]
    assert _.assoc({}, 'a', 1) == {'a': 1}


def test_assoc_in():
    assert _.assoc_in([[2]], [0, 0], 1) == [[1]]
    assert _.assoc_in([], [0, 0], 1) == [{0: 1}]
    assert _.assoc_in({}, ['a', 'b', 'c'], 12) == {'a': {'b': {'c': 12}}}
