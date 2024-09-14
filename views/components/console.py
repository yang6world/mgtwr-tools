from PyQt5.QtWidgets import QTextEdit, QFileDialog

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
        self._buffer = ""  # 用于缓存未完成的输出行

    def write(self, message):
        """
        将输出追加到文本控件中，处理缓冲区和换行符。
        """
        # 将新消息追加到缓存中
        self._buffer += message


        # 如果存在换行符，处理完整的行
        while '\n' in self._buffer:
            line, self._buffer = self._buffer.split('\n', 1)  # 分离出完整的一行
            self.append(line)  # 插入完整的行并换行

        # 如果还没有遇到换行符，数据留在缓存中

    def flush(self):
        """
        如果有未输出的内容，进行处理。这个函数会在需要刷新时被调用。
        """
        if self._buffer:
            # 输出缓存的内容（模拟为换行）
            self.append(self._buffer)
            self._buffer = ""

    def clear(self):
        """清空控制台"""
        self.setText("")

    def save(self):
        """保存控制台输出到文件"""
        file_path, _ = QFileDialog.getSaveFileName(self, "保存输出", "", "文本文件 (*.txt)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.toPlainText())



