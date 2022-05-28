# python-final
my final project of the course Programming in Python at NCU

## Virtual environment
### Creation
python3 -m venv project
### Activation
source project/bin/activate (in bash or zsh; linux or mac)  
.\project\Scripts\activate.bat (in powershell or cmd; Windows)

## Installing project requirements
pip install -r requirements.txt


## References
https://keras.io/api/applications/resnet/#resnet50-function
https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/ImageDataGenerator
https://www.tensorflow.org/api_docs/python/tf/keras/utils/load_img
https://www.tensorflow.org/api_docs/python/tf/keras/utils/img_to_array
https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet50/preprocess_input
[Source of coffee.qss](https://code.qt.io/cgit/qt/qtbase.git/tree/examples/widgets/widgets/stylesheet/qss/coffee.qss?h=6.3)  
[Qt for Python Official Website](https://doc.qt.io/qtforpython/index.html)

## Environment
<!-- Linux Distribution: Ubuntu-20.04  
Kernel version: 5.10.102.1-microsoft-standard-WSL2 -->
Windows 10 21H2 build 19044.1706

## Python files

#### main.py
main.py is the entry point of gui application  
It will import MainWindow() from ui_mainwindow.py and then display it.
#### ui_mainwindow.py
The class Window is responsible for display image and buttons.  
QImageReader.read() returns a QImage and then _set_image(QImage) will set the QLabel and display the QLabel image.  
**dialog.selectedFiles()[0]** will be the absolute path of the selected file.  
The selected image file will be opened or saved.  

#### mainwindow.ui
ui file is generated by pyside6-designer which is a GUI designer.  
ui_mainwindow.py is generated by pyside6-uic which is a (*.ui) XML compiler.

## Screenshot
![screenshot](https://user-images.githubusercontent.com/76196301/170625813-56fb155d-6107-4a99-8772-4a4a3eb1a5f3.png)
