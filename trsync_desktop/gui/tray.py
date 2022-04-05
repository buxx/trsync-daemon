from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QDialog


class SystemTray(QSystemTrayIcon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icon = QIcon("icon.png")
        self.setIcon(icon)
        self.setVisible(True)
