"""PySide6 port of the widgets/imageviewer example from Qt v6.0"""

import sys

# from PySide6.QtGui import (QAction, QClipboard, QColorSpace, QGuiApplication,
#                            QImage, QImageReader, QImageWriter, QKeySequence,
#                            QPalette, QPainter, QPixmap, QScreen)
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel,
                               QMainWindow, QMenuBar, QMessageBox, QScrollArea,
                               QScrollBar, QSizePolicy, QStatusBar, QDockWidget)
from PySide6.QtCore import Qt
from mainwindow import Window

if __name__ == '__main__':
    # arg_parser = ArgumentParser(description="Image Viewer",
    #                             formatter_class=RawTextHelpFormatter)
    # arg_parser.add_argument('file', type=str, nargs='?', help='Image file')
    # args = arg_parser.parse_args()

    app = QApplication(sys.argv)
    # image_viewer = ImageViewer(application=app)
    main_window = Window(application=app)
    main_window.show()
    # dialog = Dialog(image_viewer=image_viewer, application=app, mode=0)
    # dialog.show()

    # if args.file and not image_viewer.load_file(args.file):
    #     sys.exit(-1)

    # image_viewer.show()
    sys.exit(app.exec())
