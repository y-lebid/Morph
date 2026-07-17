import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from ui.main_window import MorphBrowser

if __name__ == "__main__":
    try:
        myappid = 'morph.browser.core.1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = QApplication(sys.argv)
    window = MorphBrowser()
    window.show()
    sys.exit(app.exec())