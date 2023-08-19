# -*- coding: utf-8 -*-

import pyperclip
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QMouseEvent


class Ui_translateWindow(QMainWindow):
    def copy_clipboard(self, event):
        text = self.translated_text_label.text().strip()
        print(f"Clipboard copy: [{text}]")
        pyperclip.copy(text)

    def __init__(self, opacity_slider):
        super().__init__()
        self.setObjectName("translateWindow")
        self.resize(800, 161)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.translated_text_label = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.translated_text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.translated_text_label, 0, 0, 1, 1)

        font = QtGui.QFont()
        font.setPointSize(12)

        self.translated_text_label.setFont(font)
        self.translated_text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.translated_text_label.setObjectName("translated_text_label")
        self.translated_text_label.setWordWrap(True)
        self.translated_text_label.mousePressEvent = self.copy_clipboard

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:black;")

    def mousePressEvent(self, event: QMouseEvent):
        try:
            self.oldPosition = event.globalPosition()
            print(self.oldPosition)
            print(type(self.oldPosition))
        except AttributeError as e:
            print(f'Cannot detect mouse press: {e}')

    # action #2
    def mouseMoveEvent(self, event: QMouseEvent):
        try:
            delta = event.globalPosition() - self.oldPosition
            delta = delta.toPoint()
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPosition()
        except AttributeError as e:
            print(f'Unable to move window: {e}')

    def set_worker(self, worker):
        self.worker = worker

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("translateWindow", "DeskTranslator - Translating"))
        self.translated_text_label.setText(_translate("translateWindow", "Translated text here"))

    def closeEvent(self, event):
        self.worker.stop_running()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    translateWindow = QtWidgets.QMainWindow()
    ui = Ui_translateWindow()
    ui.setupUi(translateWindow)
    translateWindow.show()
    sys.exit(app.exec_())
