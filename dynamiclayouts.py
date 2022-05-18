"""PySide6 port of the widgets/layouts/dynamiclayouts example from Qt v5.x"""

from argparse import ArgumentParser, RawTextHelpFormatter
import sys

from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtWidgets import (QApplication, QDialog, QLayout, QGridLayout,
                               QMessageBox, QGroupBox, QSpinBox, QSlider,
                               QProgressBar, QDial, QDialogButtonBox,
                               QComboBox, QLabel, QMainWindow)


arg_parser = ArgumentParser(description="Image Viewer",
                                formatter_class=RawTextHelpFormatter)
arg_parser.add_argument('file', type=str, nargs='?', help='Image file')
args = arg_parser.parse_args()

class Dialog(QDialog):
    def __init__(self, image_viewer, application, mode):
        super().__init__()
        self.mode = mode
        self.app = application
        self.image_viewer = image_viewer
        self._image_label = QLabel()
        if (mode != 0):
            self._image_label = image_viewer._image_label
        else:
            self.widgets = []

            # self.create_rotable_group_box()
            # self.create_options_group_box()
            self.create_button_box()
            self.label = QLabel("Click Classify or Attack and then choose an image")
            main_layout = QGridLayout()
            main_layout.addWidget(self.label, 0, 0)
            # main_layout.addWidget(self._rotable_group_box, 0, 0)
            # main_layout.addWidget(self._image_label, 1, 0)
            main_layout.addWidget(self._button_box, 2, 0)
            main_layout.setSizeConstraint(QLayout.SetMaximumSize)

            self._main_layout = main_layout
            self.setLayout(self._main_layout)

            self.setWindowTitle("Adversarial Attacker")


    def show_help(self):
        QMessageBox.information(self, "Dynamic Layouts Help",
                            "This example shows how to change layouts "
                            "dynamically.")
    def classify(self):
        self.mode = 1
        # app = QApplication(sys.argv)
        # image_viewer = ImageViewer()
        if args.file and not self.image_viewer.load_file(args.file):
            sys.exit(-1)
        self.image_viewer.show()
        self.image_viewer.activateWindow()
        self.image_viewer.setFocus()
        self._image_label = self.image_viewer._image_label
        
        # self._image_label = self.image_viewer._image_label
        # self.setLayout(self._main_layout)
        # self.app.setActiveWindow(self.image_viewer)
        # sys.exit(app.exec())

    def attack(self):
        self.mode = 2
        # app = QApplication(sys.argv)
        # image_viewer = ImageViewer()
        if args.file and not self.image_viewer.load_file(args.file):
            sys.exit(-1)
        self.image_viewer.activateWindow()
        self.image_viewer.show()
        # sys.exit(app.exec())

    # def create_rotable_group_box(self):
    #     self._rotable_group_box = QGroupBox("Click Classify or Attack and then choose an image")
    #     # self.widgets.append(self._image_label)
    #     # self.widgets.append(QSpinBox())
    #     # self.widgets.append(QSlider())
    #     # self.widgets.append(QDial())
    #     # self.widgets.append(QProgressBar())
    #     # count = len(self.widgets)
    #     # for i in range(count):
    #     #     element = self.widgets[(i + 1) % count]
    #     #     self.widgets[i].valueChanged[int].connect(element.setValue)

    #     self._rotable_layout = QGridLayout()
    #     self._rotable_group_box.setLayout(self._rotable_layout)

        # self.rotate_widgets()

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

    @Slot()
    def accept(self) -> None:
        
        return super().done(self.mode)
    # @Slot()
    # def _classify():
        
    # @Slot()
    # def _attack():

    # def rotate_widgets(self):
    #     count = len(self.widgets)
    #     if count % 2 == 1:
    #         raise AssertionError("Number of widgets must be even")

    #     for widget in self.widgets:
    #         self._rotable_layout.removeWidget(widget)

    #     self.widgets.append(self.widgets.pop(0))

    #     for i in range(count // 2):
    #         self._rotable_layout.addWidget(self.widgets[count - i - 1], 0, i)
    #         self._rotable_layout.addWidget(self.widgets[i], 1, i)

    # def buttons_orientation_changed(self, index):
    #     self._main_layout.setSizeConstraint(QLayout.SetNoConstraint)
    #     self.setMinimumSize(0, 0)

    #     orientation = Qt.Orientation(int(self._buttons_orientation_combo_box.itemData(index)))

    #     if orientation == self._button_box.orientation():
    #         return

    #     self._main_layout.removeWidget(self._button_box)

    #     spacing = self._main_layout.spacing()

    #     old_size_hint = self._button_box.sizeHint() + QSize(spacing, spacing)
    #     self._button_box.setOrientation(orientation)
    #     new_size_hint = self._button_box.sizeHint() + QSize(spacing, spacing)

    #     if orientation == Qt.Horizontal:
    #         self._main_layout.addWidget(self._button_box, 2, 0)
    #         self.resize(self.size() + QSize(-old_size_hint.width(), new_size_hint.height()))
    #     else:
    #         self._main_layout.addWidget(self._button_box, 0, 3, 2, 1)
    #         self.resize(self.size() + QSize(new_size_hint.width(), -old_size_hint.height()))

    #     self._main_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

    # def create_options_group_box(self):
    #     self._options_group_box = QGroupBox("Options")

    #     buttons_orientation_label = QLabel("Orientation of buttons:")

    #     buttons_orientation_combo_box = QComboBox()
    #     buttons_orientation_combo_box.addItem("Horizontal", Qt.Horizontal)
    #     buttons_orientation_combo_box.addItem("Vertical", Qt.Vertical)
    #     buttons_orientation_combo_box.currentIndexChanged[int].connect(self.buttons_orientation_changed)

    #     self._buttons_orientation_combo_box = buttons_orientation_combo_box

    #     options_layout = QGridLayout()
    #     options_layout.addWidget(buttons_orientation_label, 0, 0)
    #     options_layout.addWidget(self._buttons_orientation_combo_box, 0, 1)
    #     options_layout.setColumnStretch(2, 1)
    #     self._options_group_box.setLayout(options_layout)

