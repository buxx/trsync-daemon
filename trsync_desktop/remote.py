import dataclasses


from dataclasses import dataclass
import typing


# TODO : change repr to hide password
@dataclasses.dataclass
class Instance:
    address: str
    username: str
    password: str
    unsecure: bool
    folder_path: typing.Optional[str] = None

    def url(self) -> str:
        scheme = "https" if not self.unsecure else "http"
        return f"{scheme}://{self.address}"


@dataclasses.dataclass
class Workspace:
    address: str
    name: str
    id: int
