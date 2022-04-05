import json
from time import time
import typing

import requests
from trsync_desktop.error import AuthenticationError, CommunicationError

from trsync_desktop.remote import Workspace

if typing.TYPE_CHECKING:
    from trsync_desktop.remote import Instance


# FIXME BS NOW : log errors
class Client:
    def __init__(self, instance: "Instance", user_id: int) -> None:
        self._instance = instance
        self._user_id = user_id

    @classmethod
    def check_credentials(cls, instance: "Instance") -> int:
        try:
            response = requests.get(
                f"{instance.url()}/api/auth/whoami",
                auth=(instance.username, instance.password),
                timeout=(5.0, 30.0),
            )
        except requests.exceptions.ConnectionError:
            raise CommunicationError()

        if response.status_code == 200:
            data = json.loads(response.content)
            return data["user_id"]

        raise AuthenticationError()

    def get_workspaces(self) -> typing.List[Workspace]:
        try:
            response = requests.get(
                f"{self._instance.url()}/api/users/{self._user_id}/workspaces",
                auth=(self._instance.username, self._instance.password),
                timeout=(5.0, 30.0),
            )
        except requests.exceptions.CommunicationError:
            raise CommunicationError()

        if response.status_code == 200:
            data = json.loads(response.content)
            return [
                Workspace(
                    name=raw["label"],
                    id=raw["workspace_id"],
                    address=self._instance.address,
                )
                for raw in data
            ]

        raise CommunicationError(
            f"Server response status code was : {response.status_code}"
        )
