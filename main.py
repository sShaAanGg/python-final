"""PySide6 port of the widgets/imageviewer example from Qt v6.0"""

import sys
import os
import PySide6
from PySide6.QtWidgets import QApplication
# from PySide6.QtCore import Qt
# from mainwindow import Window
from ui_mainwindow import MainWindow


dirname = os.path.dirname(PySide6.__file__)

plugin_path = os.path.join(dirname, 'plugins', 'platforms')

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path




if __name__ == '__main__':
    # arg_parser = ArgumentParser(description="Image Viewer",
    #                             formatter_class=RawTextHelpFormatter)
    # arg_parser.add_argument('file', type=str, nargs='?', help='Image file')
    # args = arg_parser.parse_args()

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    with open("qss/coffee.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # main_window = Window(application=app)
    # main_window.show()

    # if args.file and not image_viewer.load_file(args.file):
    #     sys.exit(-1)

    sys.exit(app.exec())
