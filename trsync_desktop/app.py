import collections
import dataclasses
import os

import pathlib
import threading
import typing

from tinydb import Query, TinyDB
from trsync_desktop.error import NotFoundError

from trsync_desktop.process import TrsyncProcess
from trsync_desktop.remote import Instance, Workspace
from trsync_desktop import utils


INSTANCE_TABLE = "instance"
WORKSPACE_TABLE = "workspace"
processUid = (str, int)


class Application:
    def __init__(self, db_file_path: pathlib.Path) -> None:
        self._processes: typing.List[TrsyncProcess] = []
        self._process_manipulation_locks: typing.DefaultDict[
            processUid, threading.Lock
        ] = collections.defaultdict(threading.Lock)
        self._db = TinyDB(db_file_path)

    def get_current_tracim_instance(self) -> typing.Optional[Instance]:
        instances_table = self._db.table(INSTANCE_TABLE)
        try:
            instance_raw = instances_table.all()[0]
            return Instance(
                address=instance_raw["address"],
                username=instance_raw["username"],
                password=instance_raw["password"],
                unsecure=instance_raw["unsecure"],
                folder_path=instance_raw["folder_path"],
            )
        except IndexError:
            return None

    def find_instance(self, address: str) -> Instance:
        # TODO : manage real search when multiple instances
        if instance := self.get_current_tracim_instance():
            return instance

        raise NotFoundError()

    def save_current_tracim_instance_address(self, instance: Instance) -> None:
        instances_table = self._db.table(INSTANCE_TABLE)
        instances_table.truncate()
        instances_table.insert(dataclasses.asdict(instance))

    def set_sync(self, instance: Instance, workspaces: typing.List[Workspace]) -> None:
        workspaces_table = self._db.table(WORKSPACE_TABLE)
        workspaces_table.remove(Query().address == instance.address)

        for workspace in workspaces:
            workspaces_table.insert(dataclasses.asdict(workspace))

        self.ensure_processes()

    def get_workspaces(self) -> typing.List[Workspace]:
        return [
            Workspace(id=doc["id"], name=doc["name"], address=doc["address"])
            for doc in self._db.table(WORKSPACE_TABLE).all()
        ]

    def ensure_processes(self) -> None:
        workspaces_to_sync: typing.List[Workspace] = self.get_workspaces()
        workspaces_to_sync_uids = [(w.address, w.id) for w in workspaces_to_sync]
        workspaces_already_sync = [
            (p.instance.address, p.workspace.id) for p in self._processes
        ]

        processes_to_stop = [
            p
            for p in self._processes
            if (p.instance.address, p.workspace.id) not in workspaces_to_sync_uids
        ]
        processes_to_start = []
        for workspace_to_sync in workspaces_to_sync:
            if (
                workspace_to_sync.address,
                workspace_to_sync.id,
            ) not in workspaces_already_sync:
                try:
                    instance = self.find_instance(workspace_to_sync.address)
                except NotFoundError:
                    pass  # TODO error
                processes_to_start.append(
                    TrsyncProcess(
                        pid=None,
                        instance=instance,
                        workspace=workspace_to_sync,
                    )
                )

        print(f"processes to start: {[p.workspace.name for p in processes_to_start]}")
        print(f"processes to stop: {[p.workspace.name for p in processes_to_stop]}")

        for process in processes_to_stop:
            threading.Thread(target=self._stop_process, args=(process,)).start()

        for process in processes_to_start:
            threading.Thread(target=self._start_process, args=(process,)).start()

    def _stop_process(self, process: TrsyncProcess) -> None:
        process_uid = (process.instance.address, process.workspace.id)
        with self._process_manipulation_locks[process_uid]:
            if process.pid is None:
                print(f"ERROR : process '{process_uid}' have no pid, aborting")
                return
            utils.stop_process(process)
        self._processes.remove(process)

    def _start_process(self, process: TrsyncProcess) -> None:
        process_uid = (process.instance.address, process.workspace.id)
        (
            pathlib.Path(process.instance.folder_path)
            / pathlib.Path(process.workspace.name)
        ).mkdir(parents=True, exist_ok=True)
        with self._process_manipulation_locks[process_uid]:
            if process.pid is not None:
                print(f"ERROR : process '{process_uid}' already have pid, aborting")
                return
            utils.start_process(process)
            process.pid = utils.find_process_pid(process)
            print(process.pid)
        self._processes.append(process)
