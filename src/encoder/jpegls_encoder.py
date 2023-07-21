import io
import time
from enum import Enum

import pillow_jpls
from PIL import Image, ImageQt
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap


class InterleaveMode(Enum):
    NONE = "none"
    LINE = "line"
    SAMPLE = "sample"


class JPEGLSEncoderWorker(QObject):
    finished = pyqtSignal(tuple)
    progress = pyqtSignal(int)

    def __init__(self, pixmap: QImage, info: dict):
        QObject.__init__(self)
        self.pixmap = pixmap
        self.info = info

    def run(self):
        """Long-running task."""
        interleave = self.info["interleave"]
        info, pixmap = JPEGLSEncoder.encode(self.pixmap, interleave)
        self.info["configuration"]["interleave"] = interleave
        self.info.update(info)
        self.finished.emit((self.info, pixmap))


class JPEGLSEncoder:
    def encode(pixmap: QImage, interleave):
        pil_im = ImageQt.fromqpixmap(pixmap)
        print("\n---------------------------------------\n")
        print("Đang mã hoá JPEG-LS...")

        non_compressed_buffer = io.BytesIO()
        pil_im.save(non_compressed_buffer, pil_im.format)
        non_compressed_size = non_compressed_buffer.tell()
        print("Kích thước ảnh trước nén:", non_compressed_size)

        compressed_buffer = io.BytesIO()

        start = time.time()
        pil_im.save(compressed_buffer, "JPEG-LS", interleave=interleave)
        end = time.time()
        compressed_size = compressed_buffer.tell()
        compressed_buffer.close()
        print("Kích thước ảnh sau nén:", compressed_size)

        print("Tỉ số nén:", non_compressed_size / compressed_size)
        print("Thời gian mã hóa: ", end - start)
        print("Kết thúc mã hoá JPEG-LS...")
        print("\n---------------------------------------\n")

        encodedImage = QImage()
        encodedImage.loadFromData(non_compressed_buffer.getvalue())
        encodedPixmap = QPixmap()
        encodedPixmap = encodedPixmap.fromImage(encodedImage)
        non_compressed_buffer.close()

        return {
            "non_compressed_size": non_compressed_size,
            "time": round(end - start, 4),
            "compressed_size": compressed_size,
            "compress_ratio": round(non_compressed_size / compressed_size, 4),
        }, encodedPixmap
