import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon, QCursor


class NavBar(QWidget):
    on_back = pyqtSignal()
    on_forward = pyqtSignal()
    on_reload = pyqtSignal()
    on_navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setObjectName("NavBar")  # Targets QWidget#NavBar in QSS

        base_dir = os.path.dirname(os.path.dirname(__file__))
        icons_dir = os.path.join(base_dir, "resources", "icons")

        self.back_btn = self._create_btn(os.path.join(icons_dir, "back.svg"))
        self.back_btn.clicked.connect(self.on_back.emit)

        self.forward_btn = self._create_btn(os.path.join(icons_dir, "forward.svg"))
        self.forward_btn.clicked.connect(self.on_forward.emit)

        self.reload_btn = self._create_btn(os.path.join(icons_dir, "reload.svg"))
        self.reload_btn.clicked.connect(self.on_reload.emit)

        self.address_bar = QLineEdit()
        self.address_bar.setObjectName("address_bar")  # Targets QLineEdit#address_bar in QSS
        self.address_bar.setPlaceholderText("Search or enter web address...")
        self.address_bar.returnPressed.connect(self._handle_return)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(12)

        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.reload_btn)
        layout.addSpacing(10)
        layout.addWidget(self.address_bar)

        self.setLayout(layout)

    def _create_btn(self, icon_path):
        btn = QPushButton()
        btn.setProperty("class", "nav_btn")
        btn.setIcon(QIcon(icon_path))
        btn.setFixedSize(36, 36)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        return btn

    def _handle_return(self):
        self.on_navigate.emit(self.address_bar.text())

    def update_url(self, url):
        self.address_bar.setText(url)