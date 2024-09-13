from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFileDialog, QComboBox, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton)

from views.components.button import ModernButton
import pandas as pd
from utils.urltools import get_resource_path
from utils.xlsx_tools import (get_province_in_base_table, filter_out_selected_provinces,
                       generate_year_for_base_table, merge_data_to_base_table,
                       save_table_to_excel)


class DataGenerationPage(QWidget):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output
        self.selected_file_path = None
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

        # Excel 文件选择
        file_button = ModernButton("选择 Excel 文件")
        file_button.clicked.connect(self.select_file)
        layout.addWidget(file_button)

        self.file_label = QLabel("未选择文件")
        layout.addWidget(self.file_label)

        # 省份多选
        province_label = QLabel("选择省份")
        layout.addWidget(province_label)

        self.province_list = QListWidget()
        self.province_list.setSelectionMode(QListWidget.MultiSelection)
        for province in get_province_in_base_table():
            item = QListWidgetItem(province)
            self.province_list.addItem(item)
        layout.addWidget(self.province_list)

        # 添加全选和取消全选按钮
        province_button_layout = QHBoxLayout()
        select_all_button = ModernButton("全选省份")
        select_all_button.clicked.connect(self.select_all_provinces)
        deselect_all_button = ModernButton("取消全选")
        deselect_all_button.clicked.connect(self.deselect_all_provinces)
        province_button_layout.addWidget(select_all_button)
        province_button_layout.addWidget(deselect_all_button)
        layout.addLayout(province_button_layout)

        # 年份输入
        year_label = QLabel("输入年份（逗号分隔或起止年份）")
        layout.addWidget(year_label)

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("例如：2020, 2021, 2022 或 起止年份 2019-2022")
        layout.addWidget(self.year_input)

        # 生成按钮
        generate_button = ModernButton("生成数据")
        generate_button.clicked.connect(self.generate_data)
        layout.addWidget(generate_button)

        # 保存按钮
        save_button = ModernButton("保存数据")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        # 用于存储生成后的表格
        self.generated_table = None

    def select_file(self):
        # 弹出文件选择框，让用户选择 Excel 文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 Excel 文件", "", "Excel 文件 (*.xlsx)")
        if file_path:
            self.selected_file_path = file_path
            self.file_label.setText(f"已选择文件: {file_path}")
            self.console_output.append(f"已选择文件: {file_path}")
        else:
            self.console_output.append("未选择文件")

    def select_all_provinces(self):
        # 全选省份
        for i in range(self.province_list.count()):
            item = self.province_list.item(i)
            item.setSelected(True)
        self.console_output.append("所有省份已全选")

    def deselect_all_provinces(self):
        # 取消全选省份
        for i in range(self.province_list.count()):
            item = self.province_list.item(i)
            item.setSelected(False)
        self.console_output.append("已取消所有省份选择")

    def generate_data(self):
        try:
            self.console_output.append("正在生成数据...")

            # 如果用户提供了自定义 Excel 文件，使用它，否则使用默认的基础表
            if self.selected_file_path:
                self.console_output.append(f"使用用户提供的 Excel 文件: {self.selected_file_path}")
                base_table = pd.read_excel(self.selected_file_path)
            else:
                self.console_output.append("使用默认的基础表")
                base_table = pd.read_excel(get_resource_path('template/provincial_latitude_longitude.xlsx'))

            # 获取用户选择的省份
            selected_province = [item.text() for item in self.province_list.selectedItems()]
            if not selected_province:
                self.console_output.append("未选择任何省份")
                return

            self.console_output.append(f"选择的省份: {selected_province}")

            # 过滤出选中的省份
            base_table = filter_out_selected_provinces(selected_province, base_table)
            self.console_output.append(f"基础表过滤完成，共 {len(base_table)} 条记录")

            # 获取用户输入的年份
            years = self.get_years_from_input(self.year_input.text())
            if not years:
                self.console_output.append("年份输入无效，请重新输入")
                return

            self.console_output.append(f"输入的年份: {years}")

            # 为基础表生成年份列
            self.generated_table = generate_year_for_base_table(years, base_table)
            self.console_output.append(f"年份生成完成，共 {len(self.generated_table)} 条记录")

            self.console_output.append("数据生成完成！")
        except Exception as e:
            self.console_output.append(f"生成数据时发生错误: {e}")

    def get_years_from_input(self, input_text):
        try:
            if '-' in input_text:
                start_year, end_year = map(int, input_text.split('-'))
                return list(range(start_year, end_year + 1))
            else:
                return [int(year.strip()) for year in input_text.split(',')]
        except ValueError:
            return None

    def save_data(self):
        if self.generated_table is None:
            self.console_output.append("没有生成数据，无法保存！")
            return

        # 弹出保存文件对话框
        file_path, _ = QFileDialog.getSaveFileName(self, "保存数据", "", "Excel 文件 (*.xlsx)")
        if file_path:
            try:
                # 保存生成的数据到 Excel
                save_table_to_excel(self.generated_table, file_path)
                self.console_output.append(f"数据已保存至 {file_path}")
            except Exception as e:
                self.console_output.append(f"保存数据时发生错误: {e}")
