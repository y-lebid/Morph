import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QIcon, QPixmap

from ui.titlebar import CustomTitleBar
from ui.navbar import NavBar
from ui.tabs import TabsManager


class MorphBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1200, 800)

        base_dir = os.path.dirname(os.path.dirname(__file__))
        icon_path = os.path.join(base_dir, "resources", "icons", "logo.png")

        if os.path.exists(icon_path):
            original_pixmap = QPixmap(icon_path)

            w = original_pixmap.width()
            h = original_pixmap.height()

            crop_factor = 0.72
            crop_w = int(w * crop_factor)
            crop_h = int(h * crop_factor)

            x = (w - crop_w) // 2
            y = (h - crop_h) // 2

            cropped_pixmap = original_pixmap.copy(x, y, crop_w, crop_h)

            self.setWindowIcon(QIcon(cropped_pixmap))


        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.title_bar = CustomTitleBar(self)
        self.navbar = NavBar(self)
        self.tabs = TabsManager(self)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("ProgressBar")
        self.progress_bar.setFixedHeight(2)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()

        self.navbar.on_back.connect(lambda: self.tabs.current_engine().back() if self.tabs.current_engine() else None)
        self.navbar.on_forward.connect(
            lambda: self.tabs.current_engine().forward() if self.tabs.current_engine() else None)
        self.navbar.on_reload.connect(
            lambda: self.tabs.current_engine().reload() if self.tabs.current_engine() else None)
        self.navbar.on_navigate.connect(
            lambda url: self.tabs.current_engine().navigate(url) if self.tabs.current_engine() else None)

        self.tabs.url_changed.connect(self.navbar.update_url)

        self.tabs.load_started.connect(self._show_progress)
        self.tabs.load_progress.connect(self.progress_bar.setValue)
        self.tabs.load_finished.connect(self.progress_bar.hide)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.tabs)

        self.tabs.layout().insertWidget(1, self.navbar)
        self.tabs.layout().insertWidget(2, self.progress_bar)

        container = QWidget()
        container.setObjectName("MainContainer")
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.load_stylesheet()

        self.tabs.add_tab("https://google.com", "Google")

    def _show_progress(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def load_stylesheet(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        qss_path = os.path.join(base_dir, "styles", "theme.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Warning: styles/theme.qss was not found at {qss_path}!")