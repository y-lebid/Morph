from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setObjectName("TitleBar")

        self.close_btn = QPushButton()
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setFixedSize(14, 14)
        self.close_btn.clicked.connect(self.parent.close)

        self.min_btn = QPushButton()
        self.min_btn.setObjectName("min_btn")
        self.min_btn.setFixedSize(14, 14)
        self.min_btn.clicked.connect(self.parent.showMinimized)

        self.max_btn = QPushButton()
        self.max_btn.setObjectName("max_btn")
        self.max_btn.setFixedSize(14, 14)
        self.max_btn.clicked.connect(self.toggle_maximize)

        self.title = QLabel("Morph")
        self.title.setObjectName("TitleLabel")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(8)

        layout.addWidget(self.close_btn)
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(self.title)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addSpacing(14 * 3 + 8 * 2)

        self.setLayout(layout)
        self.start_pos = None

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if isinstance(child, QPushButton):
            self.start_pos = None
        elif event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.start_pos:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.start_pos = None
        super().mouseReleaseEvent(event)