# python-final
my final project of the course Programming in Python at NCU

## Virtual Environment
python3 -m venv project  
source project/bin/activate

## Installing project requirements
pip install -r requirements.txt

## python files

#### main.py
main.py is the entry point of gui application  
It will import Window() from mainwindow.py and then display it (by calling main_window.show()).
#### mainwindow.py
The class Window is responsible for display image and buttons.
QImageReader.read() returns a QImage and then _set_image(QImage) will set the QLabel and display the QLabel image.

