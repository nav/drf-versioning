import typing
from django import http
from api import transformations

_versions = []


class Version:
    def __init__(self, name: str, next: typing.Optional["Version"] = None):
        self.name = name
        self.transformations: typing.List[transformations.BaseTransformation] = []
        self.next = next

        _versions.append(self)

    def __repr__(self):
        return f'<Version (name="{self.name}")>'

    def register_transformation(self, transformation):
        if transformation in self.transformations:
            return
        self.transformations.append(transformation)
        print(self.transformations)

    @classmethod
    def by_name(cls, name):
        for v in _versions:
            if v.name == name:
                return v
        raise Exception("Invalid version requested.")

    @classmethod
    def get_stable(cls):
        return _versions[0]

    @classmethod
    def get_root(cls):
        return _versions[-1]


v2 = Version(name="v2")
v1 = Version(name="v1", next=v2)