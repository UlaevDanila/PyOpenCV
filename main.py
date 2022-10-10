import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Contours

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Графики')
        self.text1 = QLabel('Загрузить файл', self)
        button_1 = QPushButton('Выбрать и обработать', self)  
        button_1.clicked.connect(self.saveFileDialog)

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Ошибка!")
        self.msg.setText("Нужно выбрать файл с любым из следующих расширений: pdf, jpg, png")
        self.msg.setIcon(QMessageBox.Warning)

        lo1 = QVBoxLayout(self)
        lo1.addWidget(self.text1)
        lo1.addWidget(button_1)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileName(self,"Выберите файл","","All Files (*);;Text Files (*.txt)", options=options)
        for fileName in fileNames:
            if fileName:
                type_file = fileName.split(".")[1]
                if type_file == 'pdf' or type_file == 'jpg' or type_file == 'jpeg' or type_file == "png":
                    Contours.main(fileName)
                else:
                    self.msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec())