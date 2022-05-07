from django.test.client import RequestFactory
import pytest
from api import versions


@pytest.fixture
def reset_versions():
    existing = versions._versions
    yield
    versions._versions = existing


def test_can_create_version(reset_versions):
    v2022_05_01 = versions.Version(name="2022-05-01")
    assert v2022_05_01.name == "2022-05-01"
    assert v2022_05_01.transformations == []
    assert v2022_05_01.prev is None


def test_can_create_next_version(reset_versions):
    v2022_05_01 = versions.Version(name="2022-05-01")
    v2022_05_02 = versions.Version(name="2022-05-02", prev=v2022_05_01)

    assert v2022_05_02.prev == v2022_05_01


def test_cannot_have_more_than_one_versions_pointing_to_same_version(reset_versions):
    v1 = versions.Version("v1")
    versions.Version("v2", prev=v1)
    with pytest.raises(ValueError):
        versions.Version("v3", prev=v1)


def test_can_register_transformation(v1, transformation, reset_versions):
    v1.register_transformation(transformation)

    # This should be ignored
    v1.register_transformation(transformation)

    assert v1.transformations == [transformation]


def test_can_get_version_from_request():
    factory = RequestFactory(HTTP_X_API_VERSION="v1")
    request = factory.request()
    assert versions.Version.from_request(request) == versions.v1


def test_cannot_get_invalid_version_from_request():
    factory = RequestFactory(HTTP_X_API_VERSION="v9999")
    request = factory.request()
    with pytest.raises(ValueError):
        versions.Version.from_request(request)


def test_cannot_get_invalid_version():
    with pytest.raises(ValueError):
        versions.Version.by_name("v99999")
