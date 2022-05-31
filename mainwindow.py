from PySide6.QtCore import (Qt, Slot, QDir, QStandardPaths, QThread, QRunnable, QThreadPool, QMutex, QMetaObject, QObject, Signal)
from PySide6.QtGui import (QPixmap, QImageReader, QGuiApplication, QImageWriter, QColorSpace)
from PySide6.QtWidgets import (QMainWindow, QFileDialog, QDialog, QMessageBox)

import cv2
from predictor import predict
from attacker import attack
from prepare_attack import prepare_attack
from random_noise import add_random_noise
from ui_mainwindow import Ui_MainWindow

class Worker(QObject):
    def __init__(self, task, img, tmp_path) -> None:
        super().__init__()
        self.task = task
        self.img = img
        self.tmp_path = tmp_path

    resultReady = Signal(tuple, tuple, tuple)
    imgReady = Signal(str)

    def run(self):
        if (self.task == "attack"):
            self.top_1, self.top_2, self.top_3 = attack(self.img)
            
        elif (self.task == "random_attack"):
            self.top_1, self.top_2, self.top_3 = attack(self.img, "random")
            
        elif (self.task == "least_likely"):
            self.top_1, self.top_2, self.top_3 = attack(self.img, "least_likely")
            
        self.resultReady.emit(self.top_1, self.top_2, self.top_3)
        self.imgReady.emit(self.tmp_path)

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
        dialog.setDirectory('test_img')
        while (dialog.exec() == QDialog.Accepted
               and not self.load_file(dialog.selectedFiles()[0])):
            pass
    
    @Slot()
    def _save_as(self):
        dialog = QFileDialog(self, "Save File As")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptSave)
        dialog.setDirectory('test_img')
        while (dialog.exec() == QDialog.Accepted
               and not self._save_file(dialog.selectedFiles()[0])):
            pass 

    def setText(self, top_1, top_2, top_3):
        self.ui.label_result.setText("top 1: " + str(top_1) + '\n' + "top 2: " + str(top_2) + '\n' + "top 3: " + str(top_3))
        self.ui.label_result.repaint()

    def setImg(self, path):
        self.adv_images_exist = 1
        self.load_file("result/result.png")
        self.img_path = path
        self.ui.button_again.show()
        self.ui.button_attack_untargeted.hide()
        self.ui.button_attack_random.hide()
        self.ui.button_attack_least.hide()
        self.ui.label_help.setText('Click "Recover" to Show Original Image')
        self.ui.label_help.repaint()

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
            self.thread = QThread()
            self.worker = Worker("attack", img, tmp_path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.resultReady.connect(self.thread.quit)
            self.worker.resultReady.connect(self.worker.deleteLater)
            self.worker.resultReady.connect(self.setText)
            self.worker.imgReady.connect(self.setImg)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
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
            self.thread = QThread()
            self.worker = Worker("random_attack", img, tmp_path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.resultReady.connect(self.thread.quit)
            self.worker.resultReady.connect(self.worker.deleteLater)
            self.worker.resultReady.connect(self.setText)
            self.worker.imgReady.connect(self.setImg)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
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
            self.thread = QThread()
            self.worker = Worker("least_likely", img, tmp_path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.resultReady.connect(self.thread.quit)
            self.worker.resultReady.connect(self.worker.deleteLater)
            self.worker.resultReady.connect(self.setText)
            self.worker.imgReady.connect(self.setImg)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
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
            self.load_file("result/random_noise_image.png")
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
        self.ui.actionNormal_size.setEnabled(enable_zoom)
    
    def _initialize_image_filedialog(self, dialog, acceptMode):
        if self._first_file_dialog:
            self._first_file_dialog = False
            # locations = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
            # directory = locations[-1] if locations else QDir.currentPath()
            dialog.setDirectory('test_img')

        mime_types = [m.data().decode('utf-8') for m in QImageWriter.supportedMimeTypes()]
        format = [m.data().decode('utf-8') for m in QImageWriter.supportedImageFormats()]
        format.sort()
        mime_types.sort()

        dialog.setMimeTypeFilters(mime_types)
        dialog.selectMimeTypeFilter("image/png")
        dialog.setAcceptMode(acceptMode)
        if acceptMode == QFileDialog.AcceptSave:
            dialog.setDefaultSuffix("png")
