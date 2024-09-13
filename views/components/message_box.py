from PyQt5.QtWidgets import QMessageBox, QPushButton


class RemindMessageBox(QMessageBox):
    def __init__(self, parent=None, icon=QMessageBox.Information, title="标题", message="内容"):
        super().__init__(parent)

        # 设置图标、标题和消息内容
        self.setIcon(icon)
        self.setWindowTitle(title)
        self.setText(message)

        # 自定义样式表
        self.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
            QMessageBox QLabel {
                color: #f0f0f0;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
            QMessageBox QPushButton:pressed {
                background-color: #3e8e41;
            }
            QMessageBox QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        # 添加标准按钮
        self.addButton(QPushButton('确定'), QMessageBox.AcceptRole)

    # 可以根据需要添加其他自定义方法
