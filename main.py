import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabBar, QStackedWidget, QSpacerItem, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MorphBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Morph")
        self.setGeometry(100, 100, 1200, 800)

        self.is_dark_mode = True

        # TABS BAR
        self.tab_bar = QTabBar()
        self.tab_bar.setDocumentMode(True)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.current_tab_changed)

        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setObjectName("new_tab_btn")
        self.new_tab_btn.setFixedSize(28, 28)
        self.new_tab_btn.setToolTip("New Tab")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab(QUrl("https://google.com"), "New Tab")) # You can replace it with your favorite one

        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(10, 8, 10, 0)
        tab_layout.setSpacing(4)
        tab_layout.addWidget(self.tab_bar)
        tab_layout.addWidget(self.new_tab_btn)
        tab_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # STACKED WIDGET
        self.stack = QStackedWidget()

        # NAVIGATION BAR
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Search or enter web address")
        self.address_bar.returnPressed.connect(self.navigate_to_url)

        self.back_btn = QPushButton("◀")
        self.back_btn.setFixedSize(30, 30)
        self.back_btn.clicked.connect(lambda: self.current_browser().back() if self.current_browser() else None)

        self.forward_btn = QPushButton("▶")
        self.forward_btn.setFixedSize(30, 30)
        self.forward_btn.clicked.connect(lambda: self.current_browser().forward() if self.current_browser() else None)

        self.reload_btn = QPushButton("⟳")
        self.reload_btn.setObjectName("reload_btn")
        self.reload_btn.setFixedSize(30, 30)
        self.reload_btn.clicked.connect(lambda: self.current_browser().reload() if self.current_browser() else None)


        self.theme_btn = QPushButton("☀")
        self.theme_btn.setObjectName("theme_btn")
        self.theme_btn.setFixedSize(30, 30)
        self.theme_btn.setToolTip("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)

        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 5, 10, 5)
        nav_layout.setSpacing(8)

        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.address_bar)
        nav_layout.addWidget(self.theme_btn)


        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(tab_layout)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.add_new_tab(QUrl("https://google.com"), "Google")
        self.apply_theme()

    # TAB LOGIC

    def add_new_tab(self, qurl, label="New Tab"):
        browser = QWebEngineView()
        browser.setUrl(qurl)

        self.stack.addWidget(browser)
        index = self.tab_bar.addTab(label)

        self.tab_bar.setTabData(index, browser)
        self.tab_bar.setCurrentIndex(index)

        browser.titleChanged.connect(lambda title, b=browser: self.update_tab_title(b, title))
        browser.urlChanged.connect(lambda qurl, b=browser: self.update_address_bar(qurl, b))

    def update_tab_title(self, browser, title):
        for i in range(self.tab_bar.count()):
            if self.tab_bar.tabData(i) == browser:
                short_title = title[:30] + "..." if len(title) > 30 else title
                self.tab_bar.setTabText(i, short_title)
                break

    def close_tab(self, index):
        if self.tab_bar.count() > 1:
            browser = self.tab_bar.tabData(index)
            self.tab_bar.removeTab(index)
            self.stack.removeWidget(browser)
            browser.deleteLater()
        else:
            self.close()

    def current_browser(self):
        return self.stack.currentWidget()

    def current_tab_changed(self, index):
        if index >= 0:
            browser = self.tab_bar.tabData(index)
            if browser:
                self.stack.setCurrentWidget(browser)
                if browser.url():
                    self.address_bar.setText(browser.url().toString())

    # NAVIGATION & THEME LOGIC

    def apply_theme(self):
        if self.is_dark_mode:
            self.theme_btn.setText("☀")  # Класичне сонце
            stylesheet = """
                QMainWindow { background-color: #0f0f0f; }
                QWidget { background-color: #1a1a1a; }
                QLineEdit { 
                    background-color: #262626; color: #e4e4e7; border: none; 
                    border-radius: 15px; padding: 0px 15px; font-size: 14px; height: 30px;
                }
                QLineEdit:focus { background-color: #333333; }
                QPushButton { 
                    background-color: transparent; color: #a1a1aa; border: none; 
                    border-radius: 4px; font-size: 16px; padding: 0px; margin: 0px;
                }
                QPushButton:hover { background-color: #333333; color: white; }

                QPushButton#new_tab_btn { font-size: 20px; }
                QPushButton#reload_btn { font-size: 20px; }
                QPushButton#theme_btn { font-size: 20px; } /* Збільшили іконку теми */

                QTabBar { background-color: transparent; border: none; }
                QTabBar::tab {
                    background-color: #1a1a1a; color: #a1a1aa;
                    padding: 8px 15px; border-top-left-radius: 8px; border-top-right-radius: 8px;
                    margin-right: 4px; min-width: 180px;
                    border: none;
                }
                QTabBar::tab:selected { background-color: #262626; color: #ffffff; border: none; }
                QTabBar::tab:hover:!selected { background-color: #333333; }
            """
        else:
            self.theme_btn.setText("☾")
            stylesheet = """
                QMainWindow { background-color: #e2e8f0; }
                QWidget { background-color: #ffffff; }
                QLineEdit { 
                    background-color: #f1f5f9; color: #1e293b; border: 1px solid #e2e8f0; 
                    border-radius: 15px; padding: 0px 15px; font-size: 14px; height: 30px;
                }
                QLineEdit:focus { background-color: #ffffff; border: 1px solid #3b82f6; }
                QPushButton { 
                    background-color: transparent; color: #64748b; border: none; 
                    border-radius: 4px; font-size: 16px; padding: 0px; margin: 0px;
                }
                QPushButton:hover { background-color: #f1f5f9; color: #0f172a; }

                QPushButton#new_tab_btn { font-size: 20px; }
                QPushButton#reload_btn { font-size: 20px; }
                QPushButton#theme_btn { font-size: 18px; font-weight: bold; } /* Місяць трохи більший */

                QTabBar { background-color: transparent; border: none; }
                QTabBar::tab {
                    background-color: #e2e8f0; color: #64748b;
                    padding: 8px 15px; border-top-left-radius: 8px; border-top-right-radius: 8px;
                    margin-right: 4px; min-width: 180px;
                    border: none;
                }
                QTabBar::tab:selected { background-color: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-bottom: none; }
                QTabBar::tab:hover:!selected { background-color: #cbd5e1; }
            """
        self.setStyleSheet(stylesheet)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def navigate_to_url(self):
        browser = self.current_browser()
        if not browser: return

        url = self.address_bar.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        browser.setUrl(QUrl(url))

    def update_address_bar(self, qurl, browser=None):
        if browser == self.current_browser():
            self.address_bar.setText(qurl.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MorphBrowser()
    window.show()
    sys.exit(app.exec())