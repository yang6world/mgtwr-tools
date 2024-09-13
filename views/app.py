import json
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QPushButton, QLabel, QFileDialog,
                             QMessageBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from reptile import make_request, get_data_pre




class ModernComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #ccc;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                selection-background-color: #4CAF50;
            }
        """)


class DirectorySelector(QWidget):
    def __init__(self):
        super().__init__()
        self.index_history = []
        self.current_zb = None
        self.combo_boxes = []
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
        """)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title_label = QLabel("国家数据爬取")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin: 20px 0;
        """)
        main_layout.addWidget(title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        main_layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.directory_layout = QVBoxLayout(self.scroll_content)

        self.choose_file_button = ModernButton("选择 Excel 文件", self)
        self.choose_file_button.setIcon(QIcon("file_icon.png"))
        self.choose_file_button.clicked.connect(self.open_file)
        main_layout.addWidget(self.choose_file_button)

        self.file_label = QLabel()
        self.file_label.setStyleSheet("color: #666; font-style: italic;")
        main_layout.addWidget(self.file_label)

        button_layout = QHBoxLayout()
        self.back_button = ModernButton('重选')
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        button_layout.addWidget(self.back_button)

        self.select_button = ModernButton('确定')
        self.select_button.clicked.connect(self.select_directory)
        button_layout.addWidget(self.select_button)

        main_layout.addLayout(button_layout)

        self.result_label = QLabel()
        self.result_label.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        """)
        main_layout.addWidget(self.result_label)

        self.setWindowTitle('国家数据爬取')
        self.setGeometry(300, 300, 500, 600)

        self.get_index_valuecode(None)

    def open_file(self):
        self.filepath, _ = QFileDialog.getOpenFileName(self, "选择 Excel 文件", "", "Excel Files (*.xlsx)")
        if self.filepath:
            self.file_label.setText(f"已选择: {self.filepath}")
            try:
                QMessageBox.information(self, "文件加载", "文件加载成功")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法加载文件: {e}")

    def get_index_valuecode(self, zb):
        params = {
            'id': zb,
            'dbcode': 'fsnd',
            'wdcode': 'zb',
            'm': 'getTree',
        }
        data = make_request(params=params)

        if data:
            new_index = {item['name']: item['id'] for item in data}
            if new_index:
                self.current_zb = zb
                self.add_combo_box(new_index)
                self.back_button.setEnabled(len(self.index_history) > 0)
            else:
                self.result_label.setText(f"已选择: {self.current_zb}")
        else:
            self.result_label.setText("获取数据失败")

    def add_combo_box(self, index):
        combo = ModernComboBox()
        combo.addItem("请选择")
        for name, id in index.items():
            combo.addItem(name, id)
        combo.currentIndexChanged.connect(self.on_combo_changed)
        self.directory_layout.addWidget(combo)
        self.combo_boxes.append(combo)
        self.index_history.append((self.current_zb, index))

    def on_combo_changed(self, index):
        if index > 0:
            combo = self.sender()
            selected_id = combo.itemData(index)
            combo_index = self.combo_boxes.index(combo)

            for i in range(len(self.combo_boxes) - 1, combo_index, -1):
                self.directory_layout.removeWidget(self.combo_boxes[i])
                self.combo_boxes[i].deleteLater()
                self.combo_boxes.pop()
                self.index_history.pop()

            self.get_index_valuecode(selected_id)

    def go_back(self):
        if self.index_history:
            self.index_history.pop()
            self.directory_layout.removeWidget(self.combo_boxes[-1])
            self.combo_boxes[-1].deleteLater()
            self.combo_boxes.pop()

            if self.index_history:
                previous_zb, previous_index = self.index_history[-1]
                self.current_zb = previous_zb
            else:
                self.current_zb = None
                self.get_index_valuecode(None)

            self.back_button.setEnabled(len(self.index_history) > 0)
            self.result_label.clear()

    def select_directory(self):
        if self.combo_boxes:
            last_combo = self.combo_boxes[-1]
            selected_index = last_combo.currentIndex()
            if selected_index > 0:
                selected_name = last_combo.currentText()
                selected_id = last_combo.itemData(selected_index)
                self.result_label.setText(f"已选择: {selected_name} (ID: {selected_id})开始爬取数据")
                try:
                    self.result_label.setText("正在爬取数据，请稍等...")
                    self.result_label.repaint()
                    self.result_label.update()
                    get_data_pre(selected_id, self.filepath)
                    self.result_label.setText("数据爬取成功")
                except Exception as e:
                    self.result_label.setText(f"爬取数据失败: {e}")
            else:
                self.result_label.setText("请在最后一个下拉菜单中进行选择")
        else:
            self.result_label.setText("没有可用的选择")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DirectorySelector()
    ex.show()
    sys.exit(app.exec_())