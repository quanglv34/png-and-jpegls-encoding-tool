import io
from enum import Enum

import pillow_jpls
from PIL import Image, ImageQt
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QImage


class InterleaveMode(Enum):
    NONE = "none"
    LINE = "line"
    SAMPLE = "sample"


class JPEGLSEncoderWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, pixmap: QImage):
        QObject.__init__(self)
        self.pixmap = pixmap

    def run(self, pixmap: QImage):
        """Long-running task."""
        JPEGLSEncoder.encode(pixmap)
        self.finished.emit()


class JPEGLSEncoder:
    def encode(pixmap: QImage):
        pil_im = ImageQt.fromqpixmap(pixmap)
        print("\n---------------------------------------\n")
        print("Đang mã hoá JPEG-LS...")

        non_compressed_buffer = io.BytesIO()
        pil_im.save(non_compressed_buffer, pil_im.format)
        non_compressed_size = non_compressed_buffer.tell()
        print("Kích thước ảnh trước nén:", non_compressed_size)

        non_compressed_buffer.close()
        compressed_buffer = io.BytesIO()
        pil_im.save(compressed_buffer, "JPEG-LS")
        compressed_size = compressed_buffer.tell()
        print("Kích thước ảnh sau nén:", compressed_size)

        print("Tỉ số nén:", non_compressed_size / compressed_size)

        print("Kết thúc mã hoá JPEG-LS...")
        print("\n---------------------------------------\n")
