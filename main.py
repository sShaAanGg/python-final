"""PySide6 port of the widgets/imageviewer example from Qt v6.0"""

import sys
import os
import PySide6
from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow


dirname = os.path.dirname(PySide6.__file__)

plugin_path = os.path.join(dirname, 'plugins', 'platforms')

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    with open("qss/coffee.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
