from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel)

from views.components.button import ModernButton


class DataGenerationPage(QWidget):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("数据生成")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin: 20px 0;
        """)
        layout.addWidget(title_label)

        generate_button = ModernButton("生成数据")
        generate_button.clicked.connect(self.generate_data)
        layout.addWidget(generate_button)

    def generate_data(self):
        # 这里添加生成数据的逻辑
        self.console_output.append("正在生成数据...")
        # 模拟数据生成过程
        for i in range(5):
            self.console_output.append(f"生成数据 {i + 1}/5")
        self.console_output.append("数据生成完成！")