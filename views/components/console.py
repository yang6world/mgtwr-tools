from PyQt5.QtWidgets import QTextEdit


class ConsoleOutput(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)
    def write(self, message):
        # 将输出追加到文本控件中
        self.append(message)
        # 自动滚动到底部
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def flush(self):
        pass  # 不需要实现