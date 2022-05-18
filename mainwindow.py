from argparse import ArgumentParser, RawTextHelpFormatter
import sys

from PySide6.QtGui import (QAction, QClipboard, QColorSpace, QGuiApplication,
                           QImage, QImageReader, QImageWriter, QKeySequence,
                           QPalette, QPainter, QPixmap, QScreen)
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel,
                               QMainWindow, QMenuBar, QMessageBox, QScrollArea,
                               QScrollBar, QSizePolicy, QStatusBar, QDockWidget, QDialogButtonBox, QPushButton, QButtonGroup)
from PySide6.QtCore import Qt, Slot, QDir, QStandardPaths
from dynamiclayouts import Dialog

arg_parser = ArgumentParser(description="Image Viewer",
                                formatter_class=RawTextHelpFormatter)
arg_parser.add_argument('file', type=str, nargs='?', help='Image file')
args = arg_parser.parse_args()

class Window(QMainWindow):
    def __init__(self, application, parent=None):
        super().__init__(parent)
        self.app = application
        self.mode = 0

        self._scale_factor = 1.0
        self._first_file_dialog = True
        self._image_label = QLabel()
        self._image_label.setBackgroundRole(QPalette.Base)
        self._image_label.setSizePolicy(QSizePolicy.Ignored,
                                       QSizePolicy.Ignored)
        self._image_label.setScaledContents(True)


        self._scroll_area = QScrollArea()
        self._scroll_area.setBackgroundRole(QPalette.Dark)
        self._scroll_area.setWidget(self._image_label)
        self._scroll_area.setVisible(False)
        self.setCentralWidget(self._scroll_area)

        self._create_actions()
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_widget)

        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)
        self.setWindowTitle("Adversarial Attacker")

    def _create_actions(self):
        self.dock_widget = QDockWidget(self)
        self.create_button_box()
        self.dock_widget.setWidget(self._button_box)
        file_menu = self.menuBar().addMenu("&File")

        self._open_act = file_menu.addAction("&Open...")
        self._open_act.triggered.connect(self._open)
        self._open_act.setShortcut(QKeySequence.Open)

        view_menu = self.menuBar().addMenu("&View")

        self._zoom_in_act = view_menu.addAction("Zoom &In (25%)")
        self._zoom_in_act.setShortcut(QKeySequence.ZoomIn)
        self._zoom_in_act.triggered.connect(self._zoom_in)
        self._zoom_in_act.setEnabled(False)

        self._zoom_out_act = view_menu.addAction("Zoom &Out (25%)")
        self._zoom_out_act.triggered.connect(self._zoom_out)
        self._zoom_out_act.setShortcut(QKeySequence.ZoomOut)
        self._zoom_out_act.setEnabled(False)

        self._normal_size_act = view_menu.addAction("&Normal Size")
        self._normal_size_act.triggered.connect(self._normal_size)
        self._normal_size_act.setShortcut("Ctrl+S")
        self._normal_size_act.setEnabled(False)

        view_menu.addSeparator()

        self._fit_to_window_act = view_menu.addAction("&Fit to Window")
        self._fit_to_window_act.triggered.connect(self._fit_to_window)
        self._fit_to_window_act.setEnabled(True)
        self._fit_to_window_act.setCheckable(True)
        self._fit_to_window_act.setShortcut("Ctrl+F")

    def create_button_box(self):
        self._button_box = QDialogButtonBox()
        classify_button = self._button_box.addButton('Classify', QDialogButtonBox.ActionRole)
        attack_button = self._button_box.addButton('Attack', QDialogButtonBox.ActionRole)
        close_button = self._button_box.addButton(QDialogButtonBox.Close)
        help_button = self._button_box.addButton(QDialogButtonBox.Help)
        # rotate_widgets_button = self._button_box.addButton("Rotate &Widgets", QDialogButtonBox.ActionRole)

        # rotate_widgets_button.clicked.connect(self.rotate_widgets)
        classify_button.clicked.connect(self.classify)
        # classify_button.clicked.connect(self.accept)
        attack_button.clicked.connect(self.attack)
        # attack_button.clicked.connect(self.accept)
        close_button.clicked.connect(self.close)
        help_button.clicked.connect(self.show_help)

    def classify(self):
        self.mode = 1
        if args.file and not self.load_file(args.file):
            sys.exit(-1)
        
        # self._image_label = self.image_viewer._image_label
        # self.setLayout(self._main_layout)
        # self.app.setActiveWindow(self.image_viewer)
        # sys.exit(app.exec())

    def attack(self):
        self.mode = 2
        if args.file and not self.load_file(args.file):
            sys.exit(-1)
        
        # sys.exit(app.exec())

    def load_file(self, fileName):
        reader = QImageReader(fileName)
        reader.setAutoTransform(True)
        new_image = reader.read()
        native_filename = QDir.toNativeSeparators(fileName)
        if new_image.isNull():
            error = reader.errorString()
            QMessageBox.information(self, QGuiApplication.applicationDisplayName(),
                                    f"Cannot load {native_filename}: {error}")
            return False
        self._set_image(new_image)
        self.setWindowFilePath(fileName)

        w = self._image.width()
        h = self._image.height()
        d = self._image.depth()
        color_space = self._image.colorSpace()
        description = color_space.description() if color_space.isValid() else 'unknown'
        message = f'Opened "{native_filename}", {w}x{h}, Depth: {d} ({description})'
        self.statusBar().showMessage(message)
        return True
    
    def _set_image(self, new_image):
        self._image = new_image
        if self._image.colorSpace().isValid():
            self._image.convertToColorSpace(QColorSpace.SRgb)
        self._image_label.setPixmap(QPixmap.fromImage(self._image))
        self._scale_factor = 1.0

        self._scroll_area.setVisible(True)
        # self._print_act.setEnabled(True)
        self._fit_to_window_act.setEnabled(True)
        self._update_actions()

        if not self._fit_to_window_act.isChecked():
            self._image_label.adjustSize()

    def show_help(self):
        QMessageBox.information(self, "Adversarial Attacker Help",
                                "Click Classify or Attack and then choose an image")
    def _update_actions(self):
        # has_image = not self._image.isNull()
        # self._save_as_act.setEnabled(has_image)
        # self._copy_act.setEnabled(has_image)
        enable_zoom = not self._fit_to_window_act.isChecked()
        self._zoom_in_act.setEnabled(enable_zoom)
        self._zoom_out_act.setEnabled(enable_zoom)
        self._normal_size_act.setEnabled(enable_zoom)

    def _scale_image(self, factor):
        self._scale_factor *= factor
        new_size = self._scale_factor * self._image_label.pixmap().size()
        self._image_label.resize(new_size)

        self._adjust_scrollbar(self._scroll_area.horizontalScrollBar(), factor)
        self._adjust_scrollbar(self._scroll_area.verticalScrollBar(), factor)

        self._zoom_in_act.setEnabled(self._scale_factor < 3.0)
        self._zoom_out_act.setEnabled(self._scale_factor > 0.333)

    def _adjust_scrollbar(self, scrollBar, factor):
        pos = int(factor * scrollBar.value()
                  + ((factor - 1) * scrollBar.pageStep() / 2))
        scrollBar.setValue(pos)

    @Slot()
    def _zoom_in(self):
        self._scale_image(1.25)

    @Slot()
    def _zoom_out(self):
        self._scale_image(0.8)

    @Slot()
    def _normal_size(self):
        self._image_label.adjustSize()
        self._scale_factor = 1.0

    @Slot()
    def _fit_to_window(self):
        fit_to_window = self._fit_to_window_act.isChecked()
        self._scroll_area.setWidgetResizable(fit_to_window)
        if not fit_to_window:
            self._normal_size()
        self._update_actions()
    
    @Slot()
    def _open(self):
        dialog = QFileDialog(self, "Open File")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptOpen)
        while (dialog.exec() == QDialog.Accepted
               and not self.load_file(dialog.selectedFiles()[0])):
            pass
    
    def _initialize_image_filedialog(self, dialog, acceptMode):
        if self._first_file_dialog:
            self._first_file_dialog = False
            locations = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
            directory = locations[-1] if locations else QDir.currentPath()
            dialog.setDirectory(directory)

        mime_types = [m.data().decode('utf-8') for m in QImageWriter.supportedMimeTypes()]
        mime_types.sort()

        dialog.setMimeTypeFilters(mime_types)
        dialog.selectMimeTypeFilter("image/jpeg")
        dialog.setAcceptMode(acceptMode)
        if acceptMode == QFileDialog.AcceptSave:
            dialog.setDefaultSuffix("jpg")

    