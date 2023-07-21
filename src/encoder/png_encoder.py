import io
import time
import typing

from PIL import Image, ImageQt
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap


class PNGEncoderWorker(QObject):
    finished = pyqtSignal(tuple)
    progress = pyqtSignal(int)

    def __init__(self, pixmap: QImage, info):
        QObject.__init__(self)
        self.pixmap = pixmap
        self.info = info

    def run(self):
        """Long-running task."""
        compress_level = self.info["compress_level"]
        info, pixmap = PNGEncoder.encode(self.pixmap, int(compress_level))
        self.info["configuration"]["compress_level"] = compress_level
        self.info.update(info)
        self.finished.emit((self.info, pixmap))


class PNGEncoder:
    def encode(pixmap: QImage, compress_level=0):
        pil_im = ImageQt.fromqpixmap(pixmap)
        print("\n---------------------------------------\n")
        print("Đang mã hoá PNG...")

        non_compressed_buffer = io.BytesIO()
        pil_im.save(non_compressed_buffer, pil_im.format)
        non_compressed_size = non_compressed_buffer.tell()
        print("Kích thước ảnh trước nén:", non_compressed_size)

        non_compressed_buffer.close()
        compressed_buffer = io.BytesIO()
        start = time.time()
        pil_im.save(compressed_buffer, "PNG", compress_level=compress_level)
        end = time.time()
        compressed_size = compressed_buffer.tell()
        print("Kích thước ảnh sau nén:", compressed_size)

        print("Tỉ số nén:", non_compressed_size / compressed_size)
        print("Thời gian mã hóa: ", end - start)
        print("Kết thúc mã hoá PNG...")
        print("\n---------------------------------------\n")

        encodedImage = QImage()
        encodedImage.loadFromData(compressed_buffer.getvalue())
        encodedPixmap = QPixmap()
        encodedPixmap = encodedPixmap.fromImage(encodedImage)

        return {
            "non_compressed_size": non_compressed_size,
            "time": round(end - start, 4),
            "compressed_size": compressed_size,
            "compress_ratio": round(non_compressed_size / compressed_size, 4),
        }, encodedPixmap
