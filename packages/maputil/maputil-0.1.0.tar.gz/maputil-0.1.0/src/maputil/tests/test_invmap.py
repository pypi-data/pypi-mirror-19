import pytest

from maputil import InvMap


@pytest.fixture
def imap(map):
    return InvMap(map)


def test_make_inv_map(map):
    inv = InvMap(map)
    assert sorted(inv.keys()) == ['one', 'three', 'two']
    assert sorted(inv.values()) == [1, 2, 3]
    assert set(inv.inv) == {1, 2, 3}
    assert inv['one'] == 1
    assert inv.inv[1] == 'one'


def test_set_inv_map_value(imap):
    imap['four'] = 4
    assert imap.inv[4] == 'four'


def test_cannot_set_value_that_breaks_bijection(imap):
    with pytest.raises(ValueError):
        imap['single'] = 1


def test_delete_key(imap):
    del imap['one']
    assert 'one' not in imap
    assert 1 not in imap.inv


def test_copy_imap(imap):
    cp = imap.copy()
    assert imap == cp
    assert imap.inv == cp.inv

    cp['zero'] = 0
    assert 'zero' not in imap
    assert 0 not in imap.inv


def test_named_invmap(map):
    Kings = InvMap.named('Kings', 'kings', 'realms')
    x = Kings({'Pele': 'soccer', 'Elvis': "rock'n'roll"})
    assert x.kings == {'Pele': 'soccer', 'Elvis': "rock'n'roll"}
    assert x.realms == {'soccer': 'Pele', "rock'n'roll": 'Elvis'}


def test_repr(imap):
    assert eval(repr(imap)) == imap
