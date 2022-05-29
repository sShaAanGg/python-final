# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
    QStatusBar, QWidget, QFileDialog, QDialog, QMessageBox, QAbstractScrollArea, QFrame)

import cv2
from predictor import predict
from attacker import attack
from prepare_attack import prepare_attack
from random_noise import add_random_noise
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
        self.ui.button_add_noise.clicked.connect(self._add_noise)
        self.ui.button_again.clicked.connect(self._recover)

        self.ui.button_attack_untargeted.clicked.connect(self._attack_untarget)
        self.ui.button_attack_random.clicked.connect(self._attack_random)
        self.ui.button_attack_least.clicked.connect(self._attack_least)
        self.ui.button_attack_untargeted.hide()
        self.ui.button_attack_random.hide()
        self.ui.button_attack_least.hide()

        self.img_path = ""
        self.adv_images_exist = 0
        self.untarget_mode = 0
        self.random_mode = 0
        self.least_mode = 0
    @Slot()
    def _open(self):
        self.adv_images_exist = 0
        dialog = QFileDialog(self, "Open File")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptOpen)
        dialog.setDirectory('./')
        while (dialog.exec() == QDialog.Accepted
               and not self.load_file(dialog.selectedFiles()[0])):
            pass
    
    @Slot()
    def _save_as(self):
        dialog = QFileDialog(self, "Save File As")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptSave)
        dialog.setDirectory('./')
        while (dialog.exec() == QDialog.Accepted
               and not self._save_file(dialog.selectedFiles()[0])):
            pass 

    @Slot()
    def _attack_untarget(self):
        if (self.mode == 1):
            self.ui.label_help.setText("Untarget Mode")
            self.ui.label_result.setText("Attacking...\nPlease wait...")
            self.ui.label_help.repaint()
            self.ui.label_result.repaint()
            img = cv2.imread(self.img_path)
            tmp_path = self.img_path
            prepare_attack(img) 
            top_1, top_2, top_3 = attack(img)
            self.adv_images_exist = 1
            self.load_file("D:/python_final/python-final/result.png")
            self.img_path = tmp_path
            self.ui.label_result.setText("top 1: " + str(top_1) + '\n' + "top 2: " + str(top_2) + '\n' + "top 3: " + str(top_3))
            self.ui.label_result.repaint()
            self.ui.button_again.show()
            self.ui.button_attack_untargeted.hide()
            self.ui.button_attack_random.hide()
            self.ui.button_attack_least.hide()
            self.ui.label_help.setText('Click "Recover" to Show Original Image')
            self.ui.label_help.repaint()
            return
    @Slot()
    def _attack_random(self):
        if (self.mode == 1):
            self.ui.label_help.setText("Random Target Mode")
            self.ui.label_result.setText("Attacking...\nPlease wait...")
            self.ui.label_help.repaint()
            self.ui.label_result.repaint()            
            img = cv2.imread(self.img_path)
            tmp_path = self.img_path
            prepare_attack(img) 
            top_1, top_2, top_3 = attack(img, "random")
            self.adv_images_exist = 1
            self.load_file("D:/python_final/python-final/result.png")
            self.img_path = tmp_path
            self.ui.label_result.setText("top 1: " + str(top_1) + '\n' + "top 2: " + str(top_2) + '\n' + "top 3: " + str(top_3))
            self.ui.label_result.repaint()
            self.ui.button_again.show()
            self.ui.button_attack_untargeted.hide()
            self.ui.button_attack_random.hide()
            self.ui.button_attack_least.hide()
            self.ui.label_help.setText('Click "Recover" to Show Original Image')
            return

    @Slot()
    def _attack_least(self):
        if (self.mode == 1):
            self.ui.label_help.setText("Least Likely Target Mode")
            self.ui.label_result.setText("Attacking...\nPlease wait...")
            self.ui.label_help.repaint()
            self.ui.label_result.repaint()
            img = cv2.imread(self.img_path)
            tmp_path = self.img_path
            prepare_attack(img) 
            top_1, top_2, top_3 = attack(img, "least_likely")
            self.adv_images_exist = 1
            self.load_file("D:/python_final/python-final/result.png")
            self.img_path = tmp_path
            self.ui.label_result.setText("top 1: " + str(top_1) + '\n' + "top 2: " + str(top_2) + '\n' + "top 3: " + str(top_3))
            self.ui.label_result.repaint()
            self.ui.button_again.show()
            self.ui.button_attack_untargeted.hide()
            self.ui.button_attack_random.hide()
            self.ui.button_attack_least.hide()
            self.ui.label_help.setText('Click "Recover" to Show Original Image')
            return

    @Slot()
    def _attack(self):

        if (self.ui.label_image.property("isActivated")):
            self.mode = 1
            self.ui.button_again.show()
            self.ui.button_attack_untargeted.show()
            self.ui.button_attack_random.show()
            self.ui.button_attack_least.show()
            self.ui.label_result.setText("")
            self.ui.label_help.setText('Choose attack mode')
            self.ui.label_result.repaint()
    
    @Slot()
    def _classify(self):
        if (self.ui.label_image.property("isActivated")):
            self.mode = 2
            # self.ui.button_attack.hide()
            print(self.img_path)
            img = cv2.imread(self.img_path)
            img = cv2.resize(img, (224, 224))
            if self.adv_images_exist == 0:
                # prepare_attack(img) 
                top_1, top_2, top_3 = predict(img)
                self.ui.label_result.setText("top 1: " + str(top_1) + '\n' + "top 2: " + str(top_2) + '\n' + "top 3: " + str(top_3))
            self.ui.button_again.show()
            self.ui.label_help.setText('Click "Recover" to Show Original Image')

    @Slot()
    def _add_noise(self):
        if (self.ui.label_image.property("isActivated")):
            self.mode = 3
            img = cv2.imread(self.img_path)
            img = cv2.resize(img, (224, 224))
            noisy_image = add_random_noise(img)
            top_1, top_2, top_3 = predict(noisy_image)
            path = self.img_path
            self.load_file("D:/python_final/python-final/random_noise_image.png")
            self.img_path = path
            self.ui.label_result.setText("top 1: " + str(top_1) + '\n' + "top 2: " + str(top_2) + '\n' + "top 3: " + str(top_3))
            self.ui.button_again.show()
            self.ui.label_help.setText('Click "Recover" to Show Original Image')

    @Slot()
    def _recover(self):
        if (self.mode != 0):
            self.mode = 0
            self.adv_images_exist = 0
            self.load_file(self.img_path)
            self.ui.label_result.setText("")
            self.ui.button_attack_untargeted.hide()
            self.ui.button_attack_random.hide()
            self.ui.button_attack_least.hide()
            self.ui.label_help.setText('Click "Classify", "Attack", or "Add Noise"')
            # self.ui.label_image.setProperty("isActivated", False)
            # self.ui.scrollArea.setVisible(False)

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
        self.ui.label_image.setProperty("isActivated", True)
        reader = QImageReader(fileName)
        # reader.setFormat('PNG')
        reader.setAutoTransform(True)
        # new_image = reader.read()
        img = cv2.imread(fileName)
        img = cv2.resize(img, (224, 224))
        cv2.imwrite(fileName, img)
        new_image = reader.read().scaled(430, 430, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
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
        self.img_path = fileName
        return True
    
    def _set_image(self, new_image):
        self.ui.button_attack.show()
        self.ui.button_classify.show()
        self.ui.button_add_noise.show()
        self.ui.button_again.show()
        self.ui.label_help.setText('Click "Classify", "Attack", or "Add Noise"')

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
        format = [m.data().decode('utf-8') for m in QImageWriter.supportedImageFormats()]
        format.sort()
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
        MainWindow.resize(800, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(600, 600))
        MainWindow.setMaximumSize(QSize(800, 800))
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
        self.label_help.setGeometry(QRect(120, 20, 560, 50))
        font = QFont()
        font.setPointSize(12)
        self.label_help.setFont(font)
        self.label_help.setAlignment(Qt.AlignCenter)
        self.label_help.setMargin(-5)
        self.button_classify = QPushButton(self.centralwidget)
        self.button_classify.setObjectName(u"button_classify")
        self.button_classify.setGeometry(QRect(70, 80, 120, 40))
        self.button_classify.setBaseSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(10)
        self.button_classify.setFont(font1)
        self.button_classify.setStyleSheet(u"")
        self.button_classify.setIconSize(QSize(16, 16))
        self.button_classify.setProperty("isActivated", False)
        self.button_attack = QPushButton(self.centralwidget)
        self.button_attack.setObjectName(u"button_attack")
        self.button_attack.setGeometry(QRect(260, 80, 120, 40))
        self.button_attack.setFont(font1)
        self.button_attack.setProperty("isActivated", False)
        self.button_again = QPushButton(self.centralwidget)
        self.button_again.setObjectName(u"button_again")
        self.button_again.setGeometry(QRect(620, 80, 120, 40))
        self.button_again.setFont(font1)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(190, 160, 440, 440))
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.label_image = QLabel()
        self.label_image.setObjectName(u"label_image")
        self.label_image.setEnabled(True)
        self.label_image.setGeometry(QRect(0, 0, 358, 358))
        self.label_image.setScaledContents(True)
        self.label_image.setProperty("isVisible", False)
        self.scrollArea.setWidget(self.label_image)
        self.button_add_noise = QPushButton(self.centralwidget)
        self.button_add_noise.setObjectName(u"button_add_noise")
        self.button_add_noise.setGeometry(QRect(440, 80, 125, 40))
        self.button_add_noise.setFont(font1)
        self.button_add_noise.setProperty("isActivated", False)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(120, 640, 560, 100))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label_result = QLabel(self.frame)
        self.label_result.setObjectName(u"label_result")
        self.label_result.setGeometry(QRect(0, 0, 560, 100))
        self.label_result.setFont(font)
        self.label_result.setTextFormat(Qt.PlainText)
        self.label_result.setAlignment(Qt.AlignCenter)
        self.label_result.setProperty("isVisible", False)
        self.button_attack_untargeted = QPushButton(self.centralwidget)
        self.button_attack_untargeted.setObjectName(u"button_attack_untargeted")
        self.button_attack_untargeted.setGeometry(QRect(50, 170, 120, 40))
        self.button_attack_untargeted.setFont(font1)
        self.button_attack_untargeted.setProperty("isActivated", False)
        self.button_attack_least = QPushButton(self.centralwidget)
        self.button_attack_least.setObjectName(u"button_attack_least")
        self.button_attack_least.setGeometry(QRect(50, 350, 120, 40))
        self.button_attack_least.setFont(font1)
        self.button_attack_least.setProperty("isActivated", False)
        self.button_attack_random = QPushButton(self.centralwidget)
        self.button_attack_random.setObjectName(u"button_attack_random")
        self.button_attack_random.setGeometry(QRect(50, 260, 120, 40))
        self.button_attack_random.setFont(font1)
        self.button_attack_random.setProperty("isActivated", False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.label_help.raise_()
        self.button_attack.raise_()
        self.button_classify.raise_()
        self.button_again.raise_()
        self.scrollArea.raise_()
        self.button_add_noise.raise_()
        self.frame.raise_()
        self.button_attack_untargeted.raise_()
        self.button_attack_least.raise_()
        self.button_attack_random.raise_()
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setAutoFillBackground(False)
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
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
        self.button_again.clicked.connect(self.button_attack.show)
        self.button_again.clicked.connect(self.button_classify.show)
        self.button_again.clicked.connect(self.button_add_noise.show)

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
        self.label_help.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Choose an image (Ctrl-O)</span></p></body></html>", None))
        self.button_classify.setText(QCoreApplication.translate("MainWindow", u"Classify(Ctrl-C)", None))
#if QT_CONFIG(shortcut)
        self.button_classify.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.button_attack.setText(QCoreApplication.translate("MainWindow", u"Attack(Ctrl-A)", None))
#if QT_CONFIG(shortcut)
        self.button_attack.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.button_again.setText(QCoreApplication.translate("MainWindow", u"Recover(F5)", None))
#if QT_CONFIG(shortcut)
        self.button_again.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.label_image.setText("")
        self.button_add_noise.setText(QCoreApplication.translate("MainWindow", u"Add Noise(Ctrl-N)", None))
#if QT_CONFIG(shortcut)
        self.button_add_noise.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.label_result.setText("")
        self.button_attack_untargeted.setText(QCoreApplication.translate("MainWindow", u"Untarget", None))
#if QT_CONFIG(shortcut)
        self.button_attack_untargeted.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.button_attack_least.setText(QCoreApplication.translate("MainWindow", u"Least Likely", None))
#if QT_CONFIG(shortcut)
        self.button_attack_least.setShortcut(QCoreApplication.translate("MainWindow", u"F3", None))
#endif // QT_CONFIG(shortcut)
        self.button_attack_random.setText(QCoreApplication.translate("MainWindow", u"Random target", None))
#if QT_CONFIG(shortcut)
        self.button_attack_random.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

