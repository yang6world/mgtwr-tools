from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from utils.urltools import get_resource_path


class DataVisualizationPage(QWidget):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output
        self.selected_file_path = None
        self.initUI()

    def initUI(self):
        # 创建图片标签
        image_label = QLabel(self)
        pixmap = QPixmap(get_resource_path("emoji.jpg"))
        print(get_resource_path("emoji.png"))
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # 创建文本标签
        text_label = QLabel("此页还未完成", self)
        text_label.setStyleSheet("""
            font-size: 64px;
            font-weight: bold;
            color: #4CAF50;
            margin: 20px 0;
        """)
        text_label.setAlignment(Qt.AlignCenter)

        # 创建垂直布局
        v_layout = QVBoxLayout()
        v_layout.addWidget(image_label)
        v_layout.addWidget(text_label)

        self.setLayout(v_layout)