import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QStackedWidget,
                             QMainWindow, QSplitter)

from views.components.button import ModernButton
from views.components.console import ConsoleOutput
from views.pages.MGTWR_analysis import MGRWRAnalysisPage
from views.pages.data_crawling import DirectorySelector
from views.pages.data_preparation import DataGenerationPage
from views.pages.data_validation.index import AdditionalWindows
from views.pages.data_visualization import DataVisualizationPage
from views.pages.task_manager import TaskManager


class MainWindow(QMainWindow):
    """主窗口，包括不同页面和功能。"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('多功能数据分析工具')
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(850, 1200)
        self.setMaximumSize(1800, 1300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建页面切换按钮
        button_layout = QHBoxLayout()
        self.data_gen_button = ModernButton("数据生成")
        self.dir_select_button = ModernButton("数据爬取")
        self.mgrwr_button = ModernButton("数据分析")
        self.data_visualization_button = ModernButton("数据可视化")
        self.task_manager_button = ModernButton("任务管理")
        self.additional_button = ModernButton("其他功能")  # 新增的页面按钮

        button_layout.addWidget(self.data_gen_button)
        button_layout.addWidget(self.dir_select_button)
        button_layout.addWidget(self.mgrwr_button)
        button_layout.addWidget(self.data_visualization_button)
        button_layout.addWidget(self.task_manager_button)
        button_layout.addWidget(self.additional_button)  # 新增的按钮

        main_layout.addLayout(button_layout)

        # 创建堆叠窗口部件
        self.stack = QStackedWidget()

        # 创建控制台输出
        self.console_output = ConsoleOutput()

        # 创建不同的页面
        self.task_manager = TaskManager()
        self.data_gen_page = DataGenerationPage(self.console_output)
        self.dir_select_page = DirectorySelector(self.console_output, self.task_manager)
        self.mgrwr_page = MGRWRAnalysisPage(self.console_output, self.task_manager)
        self.data_visualization_page = DataVisualizationPage(self.console_output)
        self.additional_page = AdditionalWindows()  # 新增的页面

        # 将页面添加到堆叠窗口部件
        self.stack.addWidget(self.data_gen_page)
        self.stack.addWidget(self.dir_select_page)
        self.stack.addWidget(self.mgrwr_page)
        self.stack.addWidget(self.data_visualization_page)
        self.stack.addWidget(self.task_manager)
        self.stack.addWidget(self.additional_page)  # 新增的页面

        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.stack)
        splitter.addWidget(self.console_output)
        splitter.setSizes([400, 200])

        main_layout.addWidget(splitter)
        console_button_layout = QHBoxLayout()
        # 创建控制台输出,清空按钮
        clear_button = ModernButton("清空控制台")
        clear_button.clicked.connect(self.console_output.clear)
        console_button_layout.addWidget(clear_button)
        # 保存按钮
        save_button = ModernButton("保存控制台输出")
        save_button.clicked.connect(self.console_output.save)
        console_button_layout.addWidget(save_button)
        main_layout.addLayout(console_button_layout)

        # 连接按钮信号
        self.data_gen_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.dir_select_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.mgrwr_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.data_visualization_button.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.task_manager_button.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.additional_button.clicked.connect(lambda: self.stack.setCurrentIndex(5))  # 新增页面切换

        # 重定向 stdout 和 stderr
        sys.stdout = self.console_output
        sys.stderr = self.console_output

    def __del__(self):
        # 恢复 stdout 和 stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
