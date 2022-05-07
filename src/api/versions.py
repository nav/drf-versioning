import typing

if typing.TYPE_CHECKING:
    from api import transformations  # pragma: no cover

_versions = []


class Version:
    API_VERSION_HEADER = "X-API-VERSION"

    def __init__(self, name: str, prev: typing.Optional["Version"] = None):
        self.name = name
        self.transformations: typing.List[transformations.BaseTransformation] = []
        self.prev = prev

        # Ensure only one version can point to another version
        for _version in _versions:
            if _version.prev == prev and prev is not None:
                raise ValueError("Each version can only have one successor.")

        _versions.append(self)

    def __repr__(self):
        return f'<Version (name="{self.name}")>'  # pragma: no cover

    def register_transformation(self, transformation):
        if transformation in self.transformations:
            return
        self.transformations.append(transformation)

    @classmethod
    def from_request(cls, request):
        version_name = request.headers.get(
            cls.API_VERSION_HEADER, cls.get_stable().name
        )
        if version_name not in Version.get_supported_version_names():
            raise ValueError(
                (
                    "Unsupported API version requested. Version needs to "
                    f"be one of {Version.get_supported_version_names()}."
                )
            )
        return cls.by_name(version_name)

    @classmethod
    def by_name(cls, name):
        for v in _versions:
            if v.name == name:
                return v
        raise ValueError(f"Version with name {name} does not exist.")

    @classmethod
    def get_stable(cls):
        return _versions[-1]

    @classmethod
    def get_supported_version_names(cls):
        return [v.name for v in _versions]


v1 = Version(name="v1")
v2 = Version(name="v2", prev=v1)
v3 = Version(name="v3", prev=v2)
