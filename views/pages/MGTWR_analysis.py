from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFileDialog, QListWidget, QListWidgetItem,
                             QComboBox, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QGridLayout)
from multiprocessing import Process, Queue, Manager
from views.components.button import ModernButton
import pandas as pd
from utils.data_analysis import DataAnalysis
from views.background_task.analysis import analysis_process
from views.components.parameter_box import creat_gtwr_param_box, creat_mgtwr_param_box


class MGRWRAnalysisPage(QWidget):
    def __init__(self, console_output, task_manager):
        super().__init__()
        self.console_output = console_output
        self.task_manager = task_manager
        self.analysis = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("MGRWR 分析")
        # 为标题添加超链接
        title_label.setText(f'<a href="about:blank">MGRWR 分析</a>')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin: 20px 0;
        """)
        layout.addWidget(title_label)

        # 文件导入
        import_button = ModernButton("导入 Excel 文件")
        import_button.clicked.connect(self.import_file)
        layout.addWidget(import_button)

        self.file_label = QLabel("未选择文件")
        layout.addWidget(self.file_label)

        # 变量选择
        grid_layout = QGridLayout()
        y_label = QLabel("选择因变量")
        grid_layout.addWidget(y_label, 0, 0)

        self.y_combo = QComboBox()
        grid_layout.addWidget(self.y_combo, 0, 1)

        x_label = QLabel("选择自变量 (多选)")
        grid_layout.addWidget(x_label, 1, 0)

        self.x_list = QListWidget()
        self.x_list.setSelectionMode(QListWidget.MultiSelection)
        grid_layout.addWidget(self.x_list, 1, 1)

        coords_label = QLabel("选择经纬度列 (多选)")
        grid_layout.addWidget(coords_label, 2, 0)

        self.coords_list = QListWidget()
        self.coords_list.setSelectionMode(QListWidget.MultiSelection)
        grid_layout.addWidget(self.coords_list, 2, 1)

        time_label = QLabel("选择时间列")
        grid_layout.addWidget(time_label, 3, 0)

        self.time_combo = QComboBox()
        grid_layout.addWidget(self.time_combo, 3, 1)

        layout.addLayout(grid_layout)

        # 模型和核函数
        model_kernel_layout = QHBoxLayout()

        model_label = QLabel("选择模型")
        model_kernel_layout.addWidget(model_label)

        self.model_combo = QComboBox()
        self.model_combo.addItems(['GTWR', 'MGTWR'])
        self.model_combo.currentIndexChanged.connect(self.update_parameters)
        model_kernel_layout.addWidget(self.model_combo)

        kernel_label = QLabel("选择核函数")
        model_kernel_layout.addWidget(kernel_label)

        self.kernel_combo = QComboBox()
        self.kernel_combo.addItems(['gaussian', 'bisquare', 'exponential'])
        model_kernel_layout.addWidget(self.kernel_combo)

        layout.addLayout(model_kernel_layout)

        # 固定带宽和带宽准则
        fixed_criterion_layout = QHBoxLayout()

        fixed_label = QLabel("固定带宽")
        fixed_criterion_layout.addWidget(fixed_label)

        self.fixed_combo = QComboBox()
        self.fixed_combo.addItems(['True', 'False'])
        fixed_criterion_layout.addWidget(self.fixed_combo)

        criterion_label = QLabel("带宽准则")
        fixed_criterion_layout.addWidget(criterion_label)

        self.criterion_combo = QComboBox()
        self.criterion_combo.addItems(['AICc', 'AIC', 'BIC', 'CV'])
        fixed_criterion_layout.addWidget(self.criterion_combo)

        layout.addLayout(fixed_criterion_layout)

        # 动态参数区域
        self.param_layout = QVBoxLayout()
        layout.addLayout(self.param_layout)

        # 开始分析按钮
        analyze_button = ModernButton("开始分析")
        analyze_button.clicked.connect(self.start_analysis)
        layout.addWidget(analyze_button)

        self.update_parameters()

        self.output_queue = Queue()
        self.queue_timer = QTimer(self)
        self.queue_timer.timeout.connect(self.read_queue)
        self.queue_timer.start(500)  # 每 500ms 读取一次队列

    def read_queue(self):
        """
        定期读取子进程的输出队列，并将内容显示到控制台。
        """
        while not self.output_queue.empty():
            message = self.output_queue.get()
            self.console_output.write(message)

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 Excel 文件", "", "Excel 文件 (*.xlsx)")
        if file_path:
            self.analysis = DataAnalysis(file_path)
            self.file_label.setText(f"已选择文件: {file_path}")
            self.console_output.append(f"已选择文件: {file_path}")
            self.populate_headers()
        else:
            self.console_output.append("未选择文件")

    def populate_headers(self):
        headers = self.analysis.get_headers()
        self.y_combo.clear()
        self.x_list.clear()
        self.coords_list.clear()
        self.time_combo.clear()

        self.y_combo.addItems(headers)
        for header in headers:
            self.x_list.addItem(QListWidgetItem(header))
            self.coords_list.addItem(QListWidgetItem(header))
        self.time_combo.addItems(headers)

    def clear_layout(self, layout):
        """递归清空布局中的所有控件和子布局"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()

                if widget is not None:
                    widget.deleteLater()  # 删除控件

                layout_item = item.layout()
                if layout_item is not None:
                    self.clear_layout(layout_item)  # 递归清除子布局

    def update_parameters(self):
        # 清空动态参数区，删除整个布局及其子控件
        self.clear_layout(self.param_layout)
        model = self.model_combo.currentText()
        if model == 'GTWR':
            # 创建 GTWR 参数输入框
            self.dynamic_inputs = creat_gtwr_param_box(self.param_layout)
        elif model == 'MGTWR':
            self.dynamic_inputs = creat_mgtwr_param_box(self.param_layout)

    def start_analysis(self):
        if self.analysis is None:
            self.console_output.append("请先导入 Excel 文件")
            return

        # 获取用户选择的变量
        y_var = self.y_combo.currentText()
        x_vars = [item.text() for item in self.x_list.selectedItems()]
        coords = [item.text() for item in self.coords_list.selectedItems()]
        t_var = self.time_combo.currentText()

        if not y_var or not x_vars or not coords or not t_var:
            self.console_output.append("请完整选择自变量、因变量、时间和经纬度列")
            return

        # 获取用户选择的核函数、固定带宽和准则
        kernel = self.kernel_combo.currentText()
        fixed = self.fixed_combo.currentText() == 'True'
        criterion = self.criterion_combo.currentText()

        # 获取动态参数输入
        model = self.model_combo.currentText()
        self.console_output.clear()
        try:
            params = {}
            if model == 'GTWR':
                params['bw_min'] = self.get_input_value_float(self.dynamic_inputs['bw_min'])
                params['bw_max'] = self.get_input_value_float(self.dynamic_inputs['bw_max'])
                params['tau_min'] = self.get_input_value_float(self.dynamic_inputs['tau_min'])
                params['tau_max'] = self.get_input_value_float(self.dynamic_inputs['tau_max'])
                params['tol'] = self.get_input_value_float(self.dynamic_inputs['tol'])
                params['bw_decimal'] = self.get_input_value_int(self.dynamic_inputs['bw_decimal'])
                params['tau_decimal'] = self.get_input_value_int(self.dynamic_inputs['tau_decimal'])
                params['max_iter'] = self.get_input_value_int(self.dynamic_inputs['max_iter'])
            elif model == 'MGTWR':
                params['bw_min'] = self.get_input_value_float(self.dynamic_inputs['bw_min'])
                params['bw_max'] = self.get_input_value_float(self.dynamic_inputs['bw_max'])
                params['tau_min'] = self.get_input_value_float(self.dynamic_inputs['tau_min'])
                params['tau_max'] = self.get_input_value_float(self.dynamic_inputs['tau_max'])
                params['multi_bw_min'] = self.get_input_value_list(self.dynamic_inputs['multi_bw_min'])
                params['multi_bw_max'] = self.get_input_value_list(self.dynamic_inputs['multi_bw_max'])
                params['multi_tau_min'] = self.get_input_value_list(self.dynamic_inputs['multi_tau_min'])
                params['multi_tau_max'] = self.get_input_value_list(self.dynamic_inputs['multi_tau_max'])
                params['tol'] = self.get_input_value_float(self.dynamic_inputs['tol'])
                params['bw_decimal'] = self.get_input_value_int(self.dynamic_inputs['bw_decimal'])
                params['tau_decimal'] = self.get_input_value_int(self.dynamic_inputs['tau_decimal'])
                params['init_bw'] = self.get_input_value_float(self.dynamic_inputs['init_bw'])
                params['init_tau'] = self.get_input_value_float(self.dynamic_inputs['init_tau'])
                params['tol_multi'] = self.get_input_value_float(self.dynamic_inputs['tol_multi'])
                params['rss_score'] = self.get_input_value_float(self.dynamic_inputs['rss_score'])






            # 启动多进程分析任务
            analysis_process_args = (
                self.analysis.file_path, y_var, x_vars, coords, t_var, kernel, fixed, criterion, model, params,
                self.output_queue
            )
            analysis_processes = Process(target=analysis_process, args=analysis_process_args)

            # 将任务添加到任务管理器
            task_id = len(self.task_manager.tasks) + 1
            self.task_manager.add_task(task_id, analysis_processes, "进程")
            # 启动进程
            analysis_processes.start()
        except Exception as e:
            self.console_output.append(f"分析时发生错误: {e}")

    def get_input_value_float(self, input_field):
        """获取用户输入的数值，如果为空则返回 None"""
        try:
            value = input_field.text().strip()
            return float(value) if value else None
        except ValueError:
            print(f"输入无效: {input_field.text()}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("输入无效")
            return None

    def get_input_value_int(self, input_field):
        """获取用户输入的数值，如果为空则返回 None"""
        try:
            value = input_field.text().strip()
            return int(value) if value else None
        except ValueError:
            print(f"输入无效: {input_field.text()}")
            # 弹出错误提示
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("输入无效")
            return None

    def get_input_value_list(self, input_field):
        """获取用户输入的数值列表，如果为空则返回 None"""
        try:
            value = input_field.text().strip(',')
            return [float(v) for v in value.split(',')] if value else None
        except ValueError:
            print(f"输入无效: {input_field.text()}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("输入无效")
            return None
