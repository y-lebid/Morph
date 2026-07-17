from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabBar, QStackedWidget, QPushButton, QSpacerItem, \
    QSizePolicy
from PyQt6.QtGui import QIcon
from core.browser_engine import MorphWebEngine


class TabsManager(QWidget):
    url_changed = pyqtSignal(str)
    # Нові сигнали для прогрес-бару
    load_started = pyqtSignal()
    load_progress = pyqtSignal(int)
    load_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TabsManager")

        self.tab_bar = QTabBar()
        self.tab_bar.setDocumentMode(True)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tab_bar.setDrawBase(False)

        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self._on_tab_changed)

        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setObjectName("new_tab_btn")
        self.new_tab_btn.setFixedSize(28, 28)
        self.new_tab_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.new_tab_btn.clicked.connect(lambda: self.add_tab("https://google.com", "New Tab"))

        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(15, 0, 15, 0)
        tab_layout.setSpacing(4)
        tab_layout.addWidget(self.tab_bar)
        tab_layout.addWidget(self.new_tab_btn)
        tab_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.stack = QStackedWidget()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(tab_layout)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def add_tab(self, url, label="Loading..."):
        engine = MorphWebEngine(url)
        engine.titleChanged.connect(lambda title, e=engine: self._update_tab_title(e, title))
        engine.urlChanged.connect(lambda qurl, e=engine: self._update_url_if_active(e, qurl))
        engine.iconChanged.connect(lambda icon, e=engine: self._update_tab_icon(e, icon))

        # Підключаємо сигнали завантаження від рушія
        engine.loadStarted.connect(lambda e=engine: self._on_load_started(e))
        engine.loadProgress.connect(lambda p, e=engine: self._on_load_progress(e, p))
        engine.loadFinished.connect(lambda ok, e=engine: self._on_load_finished(e))

        self.stack.addWidget(engine)
        index = self.tab_bar.addTab(label)
        self.tab_bar.setTabData(index, engine)
        self.tab_bar.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tab_bar.count() > 1:
            engine = self.tab_bar.tabData(index)
            self.tab_bar.removeTab(index)
            self.stack.removeWidget(engine)
            engine.deleteLater()
        else:
            self.window().close()

    def current_engine(self):
        return self.stack.currentWidget()

    def _on_tab_changed(self, index):
        if index >= 0:
            engine = self.tab_bar.tabData(index)
            if engine:
                self.stack.setCurrentWidget(engine)
                if engine.url():
                    self.url_changed.emit(engine.url().toString())
                # Оновлюємо смужку, якщо вкладка ще вантажиться
                if engine.is_loading:
                    self.load_started.emit()
                    self.load_progress.emit(engine.current_progress)
                else:
                    self.load_finished.emit()

    def _update_tab_title(self, engine, title):
        for i in range(self.tab_bar.count()):
            if self.tab_bar.tabData(i) == engine:
                short_title = title[:25] + "..." if len(title) > 25 else title
                self.tab_bar.setTabText(i, short_title)
                break

    def _update_url_if_active(self, engine, qurl):
        if engine == self.current_engine():
            self.url_changed.emit(qurl.toString())

    def _update_tab_icon(self, engine, icon):
        for i in range(self.tab_bar.count()):
            if self.tab_bar.tabData(i) == engine:
                if not icon.isNull():
                    self.tab_bar.setTabIcon(i, icon)
                break

    # Обробники завантаження
    def _on_load_started(self, engine):
        if engine == self.current_engine():
            self.load_started.emit()

    def _on_load_progress(self, engine, progress):
        if engine == self.current_engine():
            self.load_progress.emit(progress)

    def _on_load_finished(self, engine):
        if engine == self.current_engine():
            self.load_finished.emit()