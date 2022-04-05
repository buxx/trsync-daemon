import typing

from PySide6.QtWidgets import QApplication

if typing.TYPE_CHECKING:
    from trsync_desktop.app import Application


class QtApplication(QApplication):
    def __init__(self, *args, app: "Application", **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setQuitOnLastWindowClosed(False)

    def sync(self):
        pass
