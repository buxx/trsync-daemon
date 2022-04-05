from dataclasses import dataclass
import typing

from trsync_desktop.remote import Instance, Workspace


@dataclass
class TrsyncProcess:
    instance: Instance
    workspace: Workspace
    pid: typing.Optional[int] = None
