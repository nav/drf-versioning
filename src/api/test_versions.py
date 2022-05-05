from api import version


def test_can_create_version():
    v2022_05_01 = version.Version(name="2022-05-01")
    assert v2022_05_01.name == "2022-05-01"
    assert v2022_05_01.transformations == []
    assert v2022_05_01.next is None
    assert v2022_05_01.prev is None


def test_can_create_next_version():
    v2022_05_01 = version.Version(name="2022-05-01")
    v2022_05_02 = version.Version(name="2022-05-02", prev=v2022_05_01)

    assert v2022_05_02.prev == v2022_05_01
