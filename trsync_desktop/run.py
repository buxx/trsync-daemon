import pathlib
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from trsync_desktop.gui.configure import show_configure_dialog

from trsync_desktop.gui.app import QtApplication as GuiApplication
from trsync_desktop.app import Application
from trsync_desktop.gui.tray import SystemTray


def run() -> None:
    # FIXME BS NOW : place db file in user app files
    db_file_path = pathlib.Path.home() / ".trsync_desktop.db"
    app = Application(db_file_path=db_file_path)
    gui = GuiApplication([], app=app)
    tray = SystemTray(gui)
    menu = QMenu()

    configure_action = QAction("Configure")
    configure_action.triggered.connect(show_configure_dialog(app))
    menu.addAction(configure_action)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(gui.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    # Start trsync processes
    app.ensure_processes()

    # Start system tray app
    gui.exec()


if __name__ == "__main__":
    run()
