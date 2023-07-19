import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QImage, QImageReader, QMovie, QPixmap, QRegion
from PyQt6.QtWidgets import QApplication, QComboBox, QGridLayout, QLabel, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Python Image Compression Tools")

        layout = QGridLayout()

        helloMsg = QLabel("<h1>Hello, World!</h1>", parent=self)
        originalImage = QLabel()
        encodedImage = QLabel()

        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["PNG", "JPEG-LS"])
        self.pageCombo.activated.connect(self.switchPage)

        layout.addWidget(helloMsg, 0, 0)
        layout.addWidget(originalImage, 1, 0)
        layout.addWidget(encodedImage, 1, 1)
        self.setLayout(layout)

        pixmap = QPixmap("data/big_tree.ppm")
        pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)
        originalImage.setPixmap(pixmap)
        originalImage.show()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
