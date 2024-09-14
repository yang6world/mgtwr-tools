from PyQt5.QtWidgets import QTextEdit, QFileDialog

from views.components.button import ModernButton


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

    def clear(self):
        self.setText("")

    def save(self):
        # 保存到文件
        file_path, _ = QFileDialog.getSaveFileName(self, "保存输出", "", "文本文件 (*.txt)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.toPlainText())