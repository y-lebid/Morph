from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings


class MorphWebEngine(QWebEngineView):

    def __init__(self, start_url="https://google.com"):
        super().__init__()

        # Внутрішні змінні стану
        self.is_loading = False
        self.current_progress = 0

        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)  # Наприклад, для PDF

        self.loadStarted.connect(self._on_load_started)
        self.loadProgress.connect(self._on_load_progress)
        self.loadFinished.connect(self._on_load_finished)

        self.setUrl(QUrl(start_url))

    def _on_load_started(self):
        self.is_loading = True
        self.current_progress = 0

    def _on_load_progress(self, progress):
        self.current_progress = progress

    def _on_load_finished(self, ok):
        self.is_loading = False
        self.current_progress = 100

    def navigate(self, url_string):

        url = url_string.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.setUrl(QUrl(url))