import io
import typing

from PIL import Image, ImageQt
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QImage


class PNGEncoderWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, pixmap: QImage):
        QObject.__init__(self)
        self.pixmap = pixmap

    def run(self):
        """Long-running task."""
        PNGEncoder.encode(self.pixmap)
        self.finished.emit()


class PNGEncoder:
    def encode(pixmap: QImage):
        pil_im = ImageQt.fromqpixmap(pixmap)
        print("\n---------------------------------------\n")
        print("Đang mã hoá PNG...")

        non_compressed_buffer = io.BytesIO()
        pil_im.save(non_compressed_buffer, pil_im.format)
        non_compressed_size = non_compressed_buffer.tell()
        print("Kích thước ảnh trước nén:", non_compressed_size)

        non_compressed_buffer.close()
        compressed_buffer = io.BytesIO()
        pil_im.save(compressed_buffer, "PNG")
        compressed_size = compressed_buffer.tell()
        print("Kích thước ảnh sau nén:", compressed_size)

        print("Tỉ số nén:", non_compressed_size / compressed_size)

        print("Kết thúc mã hoá PNG...")
        print("\n---------------------------------------\n")
