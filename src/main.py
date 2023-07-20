import sys
from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QImage, QImageReader, QMovie, QPixmap, QRegion
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStackedLayout,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class OutputTableColumns(Enum):
    INPUT_FILE_NAME = "File name"
    CONFIGURATION = "Configuration"
    ORIGINAL_SIZE = "Original Size"
    COMPRESSED_SIZE = "Compressed Size"
    COMPRESSION_RATIO = "Compression Ratio"
    ENCODED_TYPE = "Encoded Type"
    INPUT_FILE_PATH = "Input File Path"
    OUTPUT_FILE_PATH = "Output File Path"


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 1280, 720)
        self.setWindowTitle("Python Image Compression Tools")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Original Image Actions
        self.originalImageActions = QHBoxLayout()

        self.openFileDialogAction = QPushButton("Select Image")
        self.openFileDialogAction.clicked.connect(self.onOpenFileDialog)

        self.rotateOriginalImageLeftAction = QPushButton("Rotate Left")
        self.rotateOriginalImageLeftAction.clicked.connect(self.onRotateLeft)

        self.rotateOriginalImageRightAction = QPushButton("Rotate Right")
        self.rotateOriginalImageRightAction.clicked.connect(self.onRotateRight)

        self.selectImageFormat = QComboBox()
        self.selectImageFormat.addItems(["Encode to PNG", "Encode to JPEG-LS"])
        self.selectImageFormat.activated.connect(self.switchPage)

        self.encodeImageAction = QPushButton("ENCODE")
        self.encodeImageAction.setStyleSheet("color:green; font-weight: 800;")

        self.originalImageActions.addWidget(self.openFileDialogAction)
        self.originalImageActions.addWidget(self.rotateOriginalImageLeftAction)
        self.originalImageActions.addWidget(self.rotateOriginalImageRightAction)
        self.originalImageActions.addWidget(self.selectImageFormat)
        self.originalImageActions.addWidget(self.encodeImageAction)
        layout.addLayout(self.originalImageActions)
        # End of Original Image Actions

        # Images container
        self.imagesContainer = QHBoxLayout()
        layout.addLayout(self.imagesContainer)

        originalImageColumn = QVBoxLayout()
        encodedImageColumn = QVBoxLayout()

        self.originalImageLabel = QLabel("Please select an image")
        self.originalImageLabel.setText("Please select an image")
        self.originalImageLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.originalImage = QLabel()
        self.originalImage.setScaledContents(True)
        # self.originalImage.setSizePolicy(
        #     QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        # )
        self.originalImage.setStyleSheet("border: 1px solid black")
        self.originalImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        originalImageColumn.addWidget(self.originalImageLabel)
        originalImageColumn.addWidget(self.originalImage)

        self.encodedImageLabel = QLabel("Encoded image")
        self.encodedImageLabel.setText("Encoded image")
        self.encodedImageLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.encodedImage = QLabel()
        self.encodedImage.setStyleSheet("border: 1px solid black")
        # self.encodedImage.setSizePolicy(
        #     QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        # )
        self.encodedImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        encodedImageColumn.addWidget(self.encodedImageLabel)
        encodedImageColumn.addWidget(self.encodedImage)

        self.imagesContainer.addLayout(originalImageColumn)
        self.imagesContainer.addLayout(encodedImageColumn)
        # End of image container

        # layout.addWidget(originalImage, 1, 0)

        self.originalPixmap = QPixmap()
        self.encodedPixmap = QPixmap()

        # # pixmap = QPixmap("data/big_tree.ppm")
        # # pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)
        # # originalImage.setPixmap(pixmap)
        # # originalImage.show()

        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        layout.addLayout(self.stackedLayout)
        # Create the first page
        self.page1 = QWidget()
        self.page1Layout = QFormLayout()
        self.page1Layout.addRow("Name:", QLineEdit())
        self.page1Layout.addRow("Address:", QLineEdit())
        self.page1.setLayout(self.page1Layout)
        self.stackedLayout.addWidget(self.page1)
        # Create the second page
        self.page2 = QWidget()
        self.page2Layout = QFormLayout()
        self.page2Layout.addRow("Job:", QLineEdit())
        self.page2Layout.addRow("Department:", QLineEdit())
        self.page2.setLayout(self.page2Layout)
        self.stackedLayout.addWidget(self.page2)

        self.outputTable = QTableWidget()
        self.outputTable.setFixedHeight(200)
        self.outputTableColumns = [
            OutputTableColumns.INPUT_FILE_NAME.value,
            OutputTableColumns.ENCODED_TYPE.value,
            OutputTableColumns.ORIGINAL_SIZE.value,
            OutputTableColumns.COMPRESSED_SIZE.value,
            OutputTableColumns.COMPRESSION_RATIO.value,
            OutputTableColumns.CONFIGURATION.value,
            OutputTableColumns.OUTPUT_FILE_PATH.value,
            OutputTableColumns.INPUT_FILE_PATH.value,
        ]
        self.outputTable.setColumnCount(len(self.outputTableColumns))
        self.outputTable.setHorizontalHeaderLabels(self.outputTableColumns)
        self.outputTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.outputTable.insertRow(0)
        layout.addWidget(self.outputTable)

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())

    def onOpenFileDialog(self):
        filePath, type = QFileDialog.getOpenFileName(self, "Select an image")
        self.originalPixmap.load(filePath)
        print("File opened: ", self.originalImage.size())
        scaledPixmap = self.originalPixmap.scaled(
            self.originalImage.size(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation,
        )
        print("Pixmap size: ", scaledPixmap.size())
        self.originalImage.setPixmap(scaledPixmap)

    def onRotateLeft(self):
        print("Scaled size ", self.originalImage.pixmap().size())
        print("Rotated Left")

    def onRotateRight(self):
        print("Rotate Right")

    # def resizeEvent(self, event):
    #     scaledSize = self.originalImage.size()
    #     scaledSize.scale(self.originalImage.size(), Qt.AspectRatioMode.KeepAspectRatio)
    #     if (
    #         not self.originalImage.pixmap()
    #         or scaledSize != self.originalImage.pixmap().size()
    #     ):
    #         self.updateLabel()

    # def updateLabel(self):
    #     print("Original image size ", self.originalImage.size())
    #     self.originalImage.setPixmap(
    #         self.originalPixmap.scaled(
    #             self.originalImage.size(),
    #             Qt.AspectRatioMode.KeepAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation,
    #         )
    #     )


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
