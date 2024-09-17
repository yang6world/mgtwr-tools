import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QListWidget, QTextEdit, QWidget, QFileDialog, \
    QListWidgetItem

from utils.urltools import get_resource_path
from views.components.button import ModernButton


class VIFWindow(QMainWindow):
    """VIF 分析窗口，允许导入 Excel 文件并选择自变量进行分析。"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Variance Inflation Factor (VIF) 分析")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon(get_resource_path("favicon.ico")))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 导入文件按钮
        self.import_button = ModernButton("导入 Excel 文件")
        self.import_button.clicked.connect(self.import_file)
        layout.addWidget(self.import_button)

        # 显示文件路径
        self.file_label = QLabel("未选择文件")
        layout.addWidget(self.file_label)

        # 显示自变量选择
        self.var_label = QLabel("选择自变量")
        layout.addWidget(self.var_label)
        self.var_list = QListWidget()
        self.var_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.var_list)

        # 分析按钮
        self.analyze_button = ModernButton("开始分析")
        self.analyze_button.clicked.connect(self.start_analysis)
        layout.addWidget(self.analyze_button)

        # 输出结果区域
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.df = None  # 用于存储导入的 DataFrame

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 Excel 文件", "", "Excel 文件 (*.xlsx)")
        if file_path:
            self.file_label.setText(f"已选择文件: {file_path}")
            self.df = pd.read_excel(file_path)
            self.populate_variable_list()

    def populate_variable_list(self):
        """将导入的 Excel 文件中的列名添加到列表中供用户选择。"""
        if self.df is not None:
            self.var_list.clear()
            for col in self.df.columns:
                item = QListWidgetItem(col)
                self.var_list.addItem(item)

    def start_analysis(self):
        """执行 VIF 分析并显示结果。"""
        if self.df is not None:
            selected_vars = [item.text() for item in self.var_list.selectedItems()]
            if not selected_vars:
                self.result_output.setText("请选择要进行分析的自变量。")
                return

            try:
                # 选择自变量的数据
                X = self.df[selected_vars]

                # 计算 VIF
                vif_data = pd.DataFrame()
                vif_data["Feature"] = X.columns
                vif_data["VIF"] = [self.calculate_vif(X.values, i) for i in range(X.shape[1])]

                # 输出结果
                self.result_output.setText("VIF 分析结果:\n" + vif_data.to_string(index=False))
            except Exception as e:
                self.result_output.setText(f"分析过程中出现错误: {str(e)}")

    def calculate_vif(self, X, i):
        """计算给定自变量的 VIF。"""
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        return variance_inflation_factor(X, i)
