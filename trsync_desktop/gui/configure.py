import typing
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QCheckBox,
    QScrollArea,
    QWidget,
    QApplication,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen

from trsync_desktop.app import Application
from trsync_desktop.client import Client
from trsync_desktop.error import AuthenticationError, CommunicationError
from trsync_desktop.remote import Instance, Workspace

DEFAULT_FOLDER_PATH = "Select folder ..."

# FIXME BS NOW : display loading text (at creation and validation)
class Configure(QDialog):
    def __init__(self, *args, app: Application, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app
        self._instance: typing.Optional[Instance] = None
        self._all_workspaces: typing.List[Workspace] = []
        self._folder_path = None

        # Gui things
        self.setWindowTitle("Configuration")
        self._layout = QVBoxLayout()
        self._scroll = QScrollArea()
        self._workspaces_checkboxes = []
        self._workspaces_checkeds = []

        self._workspaces_widget = QWidget()
        self._workspaces_vbox = QVBoxLayout()
        if instance := self._app.get_current_tracim_instance():
            self._instance = instance
            self.refresh_workspaces()
        else:
            self._instance = Instance(
                address="mon.tracim.fr",
                username="username",
                password="password",
                unsecure=False,
                folder_path=None,
            )

        # Create widgets
        self._tracim_address = QLineEdit(self._instance.address)
        self._tracim_username = QLineEdit(self._instance.username)
        self._tracim_password = QLineEdit(self._instance.password)
        self._tracim_password.setEchoMode(QLineEdit.Password)
        self._tracim_unsecure = QCheckBox("Unsecure")
        self._tracim_unsecure.setChecked(self._instance.unsecure)
        self._folder_path = QLabel(self._instance.folder_path or DEFAULT_FOLDER_PATH)
        self._select_folder_path = QPushButton("Select folder")
        self._validate_button = QPushButton("Validate connection information")
        self._workspaces_label = QLabel("Shared Spaces")
        self._validate_workspaces = QPushButton("Validate shared spaces")

        # Create layout and add widgets
        self._layout.addWidget(self._tracim_address)
        self._layout.addWidget(self._tracim_username)
        self._layout.addWidget(self._tracim_password)
        self._layout.addWidget(self._tracim_unsecure)
        self._layout.addWidget(self._folder_path)
        self._layout.addWidget(self._select_folder_path)
        self._layout.addWidget(self._validate_button)
        self._layout.addWidget(self._workspaces_label)
        self._layout.addWidget(self._scroll)
        self._layout.addWidget(self._validate_workspaces)

        # Set dialog layout
        self.setLayout(self._layout)

        # Connect buttons
        self._validate_button.clicked.connect(self.validate_form)
        self._select_folder_path.clicked.connect(self.select_folder_path)
        self._validate_workspaces.clicked.connect(self.validate_workspaces)

        # Size and center window
        self.resize(450, 600)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        self.frameGeometry().moveCenter(center)

    def validate_form(self):
        if self._folder_path.text() == DEFAULT_FOLDER_PATH:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Configuration error")
            dlg.setText("You must select a folder where synchronize shared spaces")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec_()
            return

        self._instance = Instance(
            address=self._tracim_address.text(),
            username=self._tracim_username.text(),
            password=self._tracim_password.text(),
            unsecure=self._tracim_unsecure.isChecked(),
            folder_path=self._folder_path.text(),
        )
        self._app.save_current_tracim_instance_address(self._instance)
        self.refresh_workspaces(confirm_success=True)

    def select_folder_path(self):
        self._folder_path.setText(QFileDialog.getExistingDirectory())

    def validate_workspaces(self):
        sync_workspaces = []

        for i in self._workspaces_checkeds:
            sync_workspaces.append(self._all_workspaces[i])

        self._app.set_sync(self._instance, sync_workspaces)

    def refresh_workspaces(self, confirm_success: bool = False) -> None:
        try:
            user_id = Client.check_credentials(self._instance)
            self._all_workspaces = Client(self._instance, user_id).get_workspaces()
            self.refresh_workspaces_widgets()

            if confirm_success:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Authentication success")
                dlg.setText("Given address and credentials seems correct")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.setIcon(QMessageBox.Information)
                dlg.exec_()

        except AuthenticationError:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Authentication error")
            dlg.setText("Given address and credentials seems incorrect")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec_()

            self._all_workspaces = []
            self.refresh_workspaces_widgets()

        except CommunicationError:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Communication error")
            dlg.setText("An error happen when communicate with Tracim (check address)")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec_()

            self._all_workspaces = []
            self.refresh_workspaces_widgets()

    def refresh_workspaces_widgets(self) -> None:
        self._workspaces_checkeds = []
        sync_workspaces = self._app.get_workspaces()

        for widget in self._workspaces_checkboxes[:]:
            widget.deleteLater()
            self._workspaces_checkboxes.remove(widget)

        for i, workspace in enumerate(self._all_workspaces):
            checkbox = QCheckBox(workspace.name)
            checked = any([wp for wp in sync_workspaces if wp.id == workspace.id])
            checkbox.setChecked(checked)
            if checked:
                self._workspaces_checkeds.append(i)
            checkbox.toggled.connect(self.on_workspace_toggled)
            self._workspaces_checkboxes.append(checkbox)

        for checkbox in self._workspaces_checkboxes:
            self._workspaces_vbox.addWidget(checkbox)

        self._workspaces_widget.setLayout(self._workspaces_vbox)

        # Scroll Area Properties
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setWidgetResizable(True)
        self._scroll.setWidget(self._workspaces_widget)

    def on_workspace_toggled(self) -> None:
        checkbox = self.sender()
        checkbox_index = None

        for i, checkbox_widget in enumerate(self._workspaces_checkboxes):
            if checkbox_widget.text() == checkbox.text():
                checkbox_index = i
                break

        assert checkbox_index is not None

        if checkbox.isChecked():
            self._workspaces_checkeds.append(checkbox_index)
        else:
            self._workspaces_checkeds.remove(checkbox_index)


def show_configure_dialog(app: Application) -> typing.Callable[[], None]:
    def _():
        dialog = Configure(app=app)
        dialog.exec_()

    return _
