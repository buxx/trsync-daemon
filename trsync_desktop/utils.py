import os
import signal
import subprocess
import time

from trsync_desktop.process import TrsyncProcess


def stop_process(process: TrsyncProcess) -> None:
    if os.name == "nt":
        _stop_windows_process(process)
    else:
        _stop_posix_process(process)


def _stop_windows_process(process: TrsyncProcess) -> None:
    assert process.pid is not None
    raise NotImplementedError()


def _stop_posix_process(process: TrsyncProcess) -> None:
    assert process.pid is not None
    os.kill(process.pid, signal.SIGTERM)


def start_process(process: TrsyncProcess) -> None:
    if os.name == "nt":
        _start_windows_process(process)
    else:
        _start_posix_process(process)


def _start_windows_process(process: TrsyncProcess) -> None:
    raise NotImplementedError()


def _start_posix_process(process: TrsyncProcess) -> None:
    args = [
        # FIXME BS NOW : correct path
        f"/home/bastiensevajol/Projets/trsync/target/debug/trsync",
        # FIXME BS NOW : normalize
        f"{process.instance.folder_path}/{process.workspace.name}",
        process.workspace.address,
        str(process.workspace.id),
        process.instance.username,
        "--env-var-pass PASSWORD",
    ]
    subprocess.Popen(
        " ".join(args),
        env={"PASSWORD": process.instance.password},
        shell=True,
        # FIXME BS NOW : log file
        # stdout=stdout,
        # stderr=stdout,
    )


def find_process_pid(process: TrsyncProcess) -> int:
    if os.name == "nt":
        return _find_windows_process_pid(process)
    else:
        return _find_posix_process_pid(process)


def _find_windows_process_pid(process: TrsyncProcess) -> int:
    raise NotImplementedError()


def _find_posix_process_pid(process: TrsyncProcess) -> int:
    start = time.time()

    while time.time() - start < 5:
        time.sleep(0.250)
        ps_process = subprocess.Popen(
            ["ps", "-eo", "pid,args"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, _ = ps_process.communicate()
        for line in stdout.splitlines():
            pid, cmdline = line.decode().strip().split(" ", 1)

            # FIXME BS NOW : normalize
            if (
                cmdline.startswith(
                    "/home/bastiensevajol/Projets/trsync/target/debug/trsync"
                )
                and f"{process.instance.folder_path}/{process.workspace.name}"
                in cmdline
            ):
                return int(pid)

    raise RuntimeError("Process not found")
