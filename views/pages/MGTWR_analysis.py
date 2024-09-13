from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel)

from views.components.button import ModernButton


class MGRWRAnalysisPage(QWidget):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("MGRWR 分析")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin: 20px 0;
        """)
        layout.addWidget(title_label)

        analyze_button = ModernButton("开始分析")
        analyze_button.clicked.connect(self.start_analysis)
        layout.addWidget(analyze_button)

    def start_analysis(self):
        # 这里添加 MGRWR 分析的逻辑
        self.console_output.append("开始 MGRWR 分析...")
        # 模拟分析过程
        for i in range(5):
            self.console_output.append(f"分析步骤 {i + 1}/5")
        self.console_output.append("MGRWR 分析完成！")
