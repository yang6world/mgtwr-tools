from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFileDialog,
                             QMessageBox, QScrollArea, QTableWidgetItem)
from PyQt5.QtCore import Qt

from utils.reptile import make_request, get_data_pre
from views.background_task.crawling import CrawlerThread
from views.components.button import ModernButton
from views.components.combobox import ModernComboBox


class DirectorySelector(QWidget):
    def __init__(self, console_output, task_manager):
        super().__init__()
        self.console_output = console_output
        self.task_manager = task_manager
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

        self.get_index_valuecode(None)

    def open_file(self):
        print("选择文件")
        self.filepath, _ = QFileDialog.getOpenFileName(self, "选择 Excel 文件", "", "Excel Files (*.xlsx)")
        if self.filepath:
            self.file_label.setText(f"已选择: {self.filepath}")
            self.console_output.append(f"选择的文件: {self.filepath}")
            try:
                QMessageBox.information(self, "文件加载", "文件加载成功")
                self.console_output.append("文件加载成功")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法加载文件: {e}")
                self.console_output.append(f"错误: 无法加载文件: {e}")

    def get_index_valuecode(self, zb):
        params = {
            'id': zb,
            'dbcode': 'fsnd',
            'wdcode': 'zb',
            'm': 'getTree',
        }
        self.console_output.append(f"正在获取数据: {params}")
        data = make_request(params=params)

        if data:
            new_index = {item['name']: item['id'] for item in data}
            if new_index:
                self.current_zb = zb
                self.add_combo_box(new_index)
                self.back_button.setEnabled(len(self.index_history) > 0)
                self.console_output.append(f"获取数据成功，添加新的下拉菜单")
            else:
                self.result_label.setText(f"已选择: {self.current_zb}")
                self.console_output.append(f"已选择: {self.current_zb}")
        else:
            self.result_label.setText("获取数据失败")
            self.console_output.append("获取数据失败")

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
            self.console_output.append("返回上一级")

    def update_console_output(self, message):
        # 这是用于更新 console_output 和 result_label 的槽
        self.console_output.append(message)
        self.result_label.setText(message)

    def start_crawler_task(self, selected_id, filepath):
        # 为任务分配唯一ID
        task_id = len(self.task_manager.tasks) + 1

        # 创建后台线程对象
        self.crawler_thread = CrawlerThread(selected_id, filepath, task_id)

        # 连接信号与槽
        self.crawler_thread.progress_signal.connect(self.update_console_output)
        self.crawler_thread.finished_signal.connect(self.on_crawler_finished)
        self.crawler_thread.error_signal.connect(self.on_crawler_error)

        # 启动线程
        self.crawler_thread.start()

        # 将任务添加到任务管理器页面
        self.task_manager.add_task(task_id, self.crawler_thread, '线程')

        # # 打开任务管理器页面（如果未打开）
        # if not self.task_manager.isVisible():
        #     self.task_manager.show()

    def on_crawler_finished(self, message):
        # 当爬虫任务完成时，更新 UI 显示任务完成消息
        self.console_output.append(message)
        self.result_label.setText(message)

        # 获取 task_manager 中的任务表
        task_id = int(message.split("任务ID: ")[-1])
        task_table = self.task_manager.task_table
        for i in range(task_table.rowCount()):
            if int(task_table.item(i, 0).text()) == task_id:
                task_table.setItem(i, 1, QTableWidgetItem("已完成"))

    def on_crawler_error(self, error_message):
        # 当爬虫任务出错时，更新 UI 显示任务出错消息
        self.console_output.append(error_message)
        self.result_label.setText(error_message)

        # 获取 task_manager 中的任务表
        task_id = int(error_message.split("任务ID: ")[-1])
        task_table = self.task_manager.task_table
        for i in range(task_table.rowCount()):
            if int(task_table.item(i, 0).text()) == task_id:
                task_table.setItem(i, 1, QTableWidgetItem("出错"))

    def select_directory(self):
        if self.combo_boxes:
            last_combo = self.combo_boxes[-1]
            selected_index = last_combo.currentIndex()
            if selected_index > 0:
                selected_name = last_combo.currentText()
                selected_id = last_combo.itemData(selected_index)
                self.result_label.setText(f"已选择: {selected_name} (ID: {selected_id})")
                self.console_output.append(f"已选择: {selected_name} (ID: {selected_id})")

                # 启动后台爬虫任务
                self.result_label.setText("正在爬取数据，请稍等...")
                self.console_output.append("正在爬取数据，请稍等...")
                self.start_crawler_task(selected_id, self.filepath)
            else:
                self.result_label.setText("请在最后一个下拉菜单中进行选择")
                self.console_output.append("请在最后一个下拉菜单中进行选择")
        else:
            self.result_label.setText("没有可用的选择")
            self.console_output.append("没有可用的选择")
