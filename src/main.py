import queue
import sys
from enum import Enum

from PyQt6.QtCore import QBuffer, QIODevice, QObject, Qt, QThread, pyqtSignal
from PyQt6.QtGui import (
    QFont,
    QIcon,
    QImage,
    QImageReader,
    QMovie,
    QPixmap,
    QRegion,
    QTransform,
)
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
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

from encoder.jpegls_encoder import JPEGLSEncoderWorker
from encoder.png_encoder import PNGEncoderWorker

# Disable Image Size limit
QImageReader.setAllocationLimit(0)


class OutputTableColumns(Enum):
    INPUT_FILE_NAME = "File name"
    CONFIGURATION = "Configuration"
    ORIGINAL_SIZE = "Original Size"
    COMPRESSED_SIZE = "Compressed Size"
    COMPRESSION_RATIO = "Compression Ratio"
    ENCODED_TYPE = "Encoded Type"
    INPUT_FILE_PATH = "Input File Path"
    OUTPUT_FILE_PATH = "Output File Path"
    TIME = "Time"


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.rotation = 0

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
        self.selectImageFormat.activated.connect(self.onSelectImageFormat)

        self.encodeImageAction = QPushButton("ENCODE")
        self.encodeImageAction.clicked.connect(self.onEncodeImage)
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
        self.originalImage.setStyleSheet("border: 1px solid black")
        self.originalImage.setFixedHeight(500)
        self.originalImage.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.originalImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        originalImageColumn.addWidget(self.originalImageLabel)
        originalImageColumn.addWidget(self.originalImage)

        self.encodedImageLabel = QLabel("Encoded image")
        self.encodedImageLabel.setText("Encoded image")
        self.encodedImageLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.encodedImage = QLabel()
        self.encodedImage.setStyleSheet("border: 1px solid black")
        self.encodedImage.setFixedHeight(500)
        self.encodedImage.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.encodedImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        encodedImageColumn.addWidget(self.encodedImageLabel)
        encodedImageColumn.addWidget(self.encodedImage)

        self.imagesContainer.addLayout(originalImageColumn)
        self.imagesContainer.addLayout(encodedImageColumn)
        # End of image container

        self.originalPixmap = QPixmap()
        self.encodedPixmap = QPixmap()

        # Create the stacked layout
        self.formatOptionsPanels = QStackedLayout()
        layout.addLayout(self.formatOptionsPanels)
        # Create the first page
        self.optionsPanelPNG = QWidget()
        optionsPanelPNGLayout = QHBoxLayout()
        self.modeOptionPNG = QComboBox()
        self.modeOptionPNG.addItems(map(str, range(0, 10)))
        optionsPanelPNGLayout.addWidget(self.modeOptionPNG)
        self.optionsPanelPNG.setLayout(optionsPanelPNGLayout)
        self.formatOptionsPanels.addWidget(self.optionsPanelPNG)

        # Create the second page
        self.optionsPanelJPEGLS = QWidget()
        optionsPanelJPEGLSLayout = QHBoxLayout()
        self.modeOptionJPEGLS = QComboBox()
        self.modeOptionJPEGLS.addItems(["none", "line", "sample"])
        optionsPanelJPEGLSLayout.addWidget(self.modeOptionJPEGLS)
        self.optionsPanelJPEGLS.setLayout(optionsPanelJPEGLSLayout)
        self.formatOptionsPanels.addWidget(self.optionsPanelJPEGLS)

        self.outputTable = QTableWidget()
        self.outputTable.setFixedHeight(200)
        self.outputTableColumns = [
            OutputTableColumns.INPUT_FILE_NAME.value,
            OutputTableColumns.ENCODED_TYPE.value,
            OutputTableColumns.ORIGINAL_SIZE.value,
            OutputTableColumns.COMPRESSED_SIZE.value,
            OutputTableColumns.COMPRESSION_RATIO.value,
            OutputTableColumns.TIME.value,
            OutputTableColumns.CONFIGURATION.value,
        ]
        self.outputTable.setColumnCount(len(self.outputTableColumns))
        self.outputTable.setHorizontalHeaderLabels(self.outputTableColumns)
        header = self.outputTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.outputTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.outputTable)

    def onSelectImageFormat(self, mode):
        print("Selected mode ", self.selectImageFormat.currentText())
        self.formatOptionsPanels.setCurrentIndex(self.selectImageFormat.currentIndex())

    def onOpenFileDialog(self):
        filePath, type = QFileDialog.getOpenFileName(self, "Select an image")
        self.originalPixmap.load(filePath)
        self.updateOriginalImage()
        self.originalImageLabel.setText(filePath)

    def updateOriginalImage(self):
        scaledPixmap = self.originalPixmap.scaled(
            self.originalImage.size(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation,
        )
        self.originalImage.setPixmap(scaledPixmap)

    def updateEncodedImage(self):
        scaledPixmap = self.encodedPixmap.scaled(
            self.encodedImage.size(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation,
        )
        self.encodedImage.setPixmap(scaledPixmap)

    def onRotateLeft(self):
        self.rotation = (self.rotation - 90) % 360
        transform = QTransform().rotate(-90)
        self.originalPixmap = self.originalPixmap.transformed(transform)
        self.updateOriginalImage()

    def onRotateRight(self):
        self.rotation = (self.rotation + 90) % 360
        transform = QTransform().rotate(90)
        self.originalPixmap = self.originalPixmap.transformed(transform)
        self.updateOriginalImage()

    def onEncodeImage(self):
        self.encodedImageLabel.setText("Encoding...")

        # Thread to handle return output from image encoding thread

        # Encode image thread
        self.thread = QThread()
        if self.selectImageFormat.currentIndex() == 0:
            info = {
                "configuration": {
                    "rotation": self.rotation,
                },
                "compress_level": self.modeOptionPNG.currentText(),
                "format": "PNG",
            }
            self.worker = PNGEncoderWorker(self.originalPixmap.toImage(), info)
        else:
            info = {
                "configuration": {
                    "rotation": self.rotation,
                },
                "interleave": self.modeOptionJPEGLS.currentText(),
                "format": "JPEG-LS",
            }
            print(self.modeOptionJPEGLS.currentData())
            self.worker = JPEGLSEncoderWorker(self.originalPixmap.toImage(), info)

        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.handleEncodedImage)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()

    def handleEncodedImage(self, result):
        info, pixmap = result
        print(info)
        self.encodedPixmap.swap(pixmap)
        self.updateEncodedImage()
        self.encodedImageLabel.setText("Done.")
        self.thread.terminate()
        self.outputTable.insertRow(0)
        self.outputTable.setItem(
            0, 0, QTableWidgetItem(self.originalImageLabel.text().split("/")[-1])
        )
        self.outputTable.setItem(0, 1, QTableWidgetItem(info["format"]))
        self.outputTable.setItem(
            0, 2, QTableWidgetItem(str(info["non_compressed_size"]))
        )
        self.outputTable.setItem(0, 3, QTableWidgetItem(str(info["compressed_size"])))
        self.outputTable.setItem(0, 4, QTableWidgetItem(str(info["compress_ratio"])))
        self.outputTable.setItem(0, 5, QTableWidgetItem(str(info["time"])))
        self.outputTable.setItem(0, 6, QTableWidgetItem(str(info["configuration"])))


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
