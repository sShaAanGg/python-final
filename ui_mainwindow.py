# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowvYaqTS.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Slot, QDir, QStandardPaths)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform, QImageReader, QGuiApplication, QImageWriter, QColorSpace)
from PySide6.QtWidgets import (QApplication, QScrollArea, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget, QFileDialog, QDialog, QMessageBox, QAbstractScrollArea)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.mode = 0
        self._scale_factor = 1.0
        self._first_file_dialog = True

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.scrollArea.setVisible(False)

        self.ui.actionOpen.triggered.connect(self._open)
        self.ui.actionSave.triggered.connect(self._save_as)
        self.ui.actionFit_to_window.triggered.connect(self._fit_to_window)
        self.ui.actionFit_to_window.setEnabled(True)
        self.ui.actionFit_to_window.setCheckable(True)
        self.ui.actionNormal_size.triggered.connect(self._normal_size)
        self.ui.actionNormal_size.setEnabled(False)

        self.ui.button_attack.clicked.connect(self._attack)
        self.ui.button_classify.clicked.connect(self._classify)
        self.ui.button_again.clicked.connect(self._recover)
    
    @Slot()
    def _open(self):
        dialog = QFileDialog(self, "Open File")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptOpen)
        while (dialog.exec() == QDialog.Accepted
               and not self.load_file(dialog.selectedFiles()[0])):
            pass
    
    @Slot()
    def _save_as(self):
        dialog = QFileDialog(self, "Save File As")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptSave)
        while (dialog.exec() == QDialog.Accepted
               and not self._save_file(dialog.selectedFiles()[0])):
            pass
    
    @Slot()
    def _attack(self):
        self.mode = 1
    
    @Slot()
    def _classify(self):
        self.mode = 2

    @Slot()
    def _recover(self):
        self.mode = 0

    @Slot()
    def _normal_size(self):
        self.ui.label_image.adjustSize()
        self._scale_factor = 1.0

    @Slot()
    def _fit_to_window(self):
        fit_to_window = self.ui.actionFit_to_window.isChecked()
        self.ui.scrollArea.setWidgetResizable(fit_to_window)
        if not fit_to_window:
            self._normal_size()
        self._update_actions()

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
        self.ui.label_image.setPixmap(QPixmap.fromImage(self._image))
        self._scale_factor = 1.0

        self.ui.scrollArea.setVisible(True)
        self.ui.actionFit_to_window.setEnabled(True)
        self._update_actions()

        if not self.ui.actionFit_to_window.isChecked():
            self.ui.label_image.adjustSize()


    def _save_file(self, fileName):
        writer = QImageWriter(fileName)

        native_filename = QDir.toNativeSeparators(fileName)
        if not writer.write(self._image):
            error = writer.errorString()
            message = f"Cannot write {native_filename}: {error}"
            QMessageBox.information(self, QGuiApplication.applicationDisplayName(),
                                    message)
            return False
        self.statusBar().showMessage(f'Wrote "{native_filename}"')
        return True
    
    def _update_actions(self):
        has_image = not self._image.isNull()
        self.ui.actionSave.setEnabled(has_image)
        enable_zoom = not self.ui.actionFit_to_window.isChecked()
        # self._zoom_in_act.setEnabled(enable_zoom)
        # self._zoom_out_act.setEnabled(enable_zoom)
        self.ui.actionNormal_size.setEnabled(enable_zoom)
    
    def _initialize_image_filedialog(self, dialog, acceptMode):
        if self._first_file_dialog:
            self._first_file_dialog = False
            locations = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
            directory = locations[-1] if locations else QDir.currentPath()
            dialog.setDirectory(directory)

        mime_types = [m.data().decode('utf-8') for m in QImageWriter.supportedMimeTypes()]
        mime_types.sort()

        dialog.setMimeTypeFilters(mime_types)
        dialog.selectMimeTypeFilter("image/png")
        dialog.setAcceptMode(acceptMode)
        if acceptMode == QFileDialog.AcceptSave:
            dialog.setDefaultSuffix("png")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 640)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(960, 640))
        MainWindow.setMouseTracking(False)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionFit_to_window = QAction(MainWindow)
        self.actionFit_to_window.setObjectName(u"actionFit_to_window")
        self.actionNormal_size = QAction(MainWindow)
        self.actionNormal_size.setObjectName(u"actionNormal_size")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.centralwidget.setAutoFillBackground(False)
        self.label_help = QLabel(self.centralwidget)
        self.label_help.setObjectName(u"label_help")
        self.label_help.setGeometry(QRect(0, 10, 951, 51))
        font = QFont()
        font.setPointSize(12)
        self.label_help.setFont(font)
        self.label_help.setAlignment(Qt.AlignCenter)
        self.label_help.setMargin(-5)
        self.button_classify = QPushButton(self.centralwidget)
        self.button_classify.setObjectName(u"button_classify")
        self.button_classify.setGeometry(QRect(280, 60, 80, 40))
        self.button_classify.setBaseSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(10)
        self.button_classify.setFont(font1)
        self.button_classify.setStyleSheet(u"")
        self.button_classify.setIconSize(QSize(16, 16))
        self.button_classify.setProperty("isActivated", False)
        self.button_attack = QPushButton(self.centralwidget)
        self.button_attack.setObjectName(u"button_attack")
        self.button_attack.setGeometry(QRect(590, 60, 80, 40))
        self.button_attack.setFont(font1)
        self.button_attack.setProperty("isActivated", False)
        self.label_result = QLabel(self.centralwidget)
        self.label_result.setObjectName(u"label_result")
        self.label_result.setGeometry(QRect(30, 540, 891, 61))
        self.label_result.setFont(font)
        self.label_result.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_result.setProperty("isVisible", False)
        self.button_again = QPushButton(self.centralwidget)
        self.button_again.setObjectName(u"button_again")
        self.button_again.setGeometry(QRect(840, 20, 81, 61))
        self.button_again.setFont(font1)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(20, 120, 911, 411))
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 909, 409))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy1)
        self.label_image = QLabel(self.scrollAreaWidgetContents_2)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setEnabled(True)
        self.label_image.setGeometry(QRect(0, 0, 909, 409))
        self.label_image.setScaledContents(True)
        self.label_image.setProperty("isVisible", False)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.label_help.raise_()
        self.button_attack.raise_()
        self.button_classify.raise_()
        self.label_result.raise_()
        self.button_again.raise_()
        self.scrollArea.raise_()
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 960, 19))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuView.addAction(self.actionFit_to_window)
        self.menuView.addAction(self.actionNormal_size)

        self.retranslateUi(MainWindow)
        self.button_classify.clicked.connect(self.button_attack.hide)
        self.button_attack.clicked.connect(self.button_classify.hide)
        self.button_again.clicked.connect(self.button_attack.show)
        self.button_again.clicked.connect(self.button_classify.show)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Adversarial Attacker", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionFit_to_window.setText(QCoreApplication.translate("MainWindow", u"Fit to window", None))
#if QT_CONFIG(shortcut)
        self.actionFit_to_window.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionNormal_size.setText(QCoreApplication.translate("MainWindow", u"Normal size", None))
        self.label_help.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Choose an image and then click 'Classify' or 'Attack'</span></p></body></html>", None))
        self.button_classify.setText(QCoreApplication.translate("MainWindow", u"Classify", None))
        self.button_attack.setText(QCoreApplication.translate("MainWindow", u"Attack", None))
        self.label_result.setText("")
        self.button_again.setText(QCoreApplication.translate("MainWindow", u"Try Again", None))
        self.label_image.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

