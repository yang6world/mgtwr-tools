import sys
import io
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QPushButton, QLabel, QFileDialog, 
                             QMessageBox, QFrame, QScrollArea, QStackedWidget,
                             QMainWindow, QTextEdit, QSplitter)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor
from reptile import make_request, get_data_pre

class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

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
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                selection-background-color: #4CAF50;
            }
        """)

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

class DataGenerationPage(QWidget):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output
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

        generate_button = ModernButton("生成数据")
        generate_button.clicked.connect(self.generate_data)
        layout.addWidget(generate_button)

    def generate_data(self):
        # 这里添加生成数据的逻辑
        self.console_output.append("正在生成数据...")
        # 模拟数据生成过程
        for i in range(5):
            self.console_output.append(f"生成数据 {i+1}/5")
        self.console_output.append("数据生成完成！")

class DirectorySelector(QWidget):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output
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
    
    def select_directory(self):
        if self.combo_boxes:
            last_combo = self.combo_boxes[-1]
            selected_index = last_combo.currentIndex()
            if selected_index > 0:
                selected_name = last_combo.currentText()
                selected_id = last_combo.itemData(selected_index)
                self.result_label.setText(f"已选择: {selected_name} (ID: {selected_id})")
                self.console_output.append(f"已选择: {selected_name} (ID: {selected_id})")
            else:
                self.result_label.setText("请在最后一个下拉菜单中进行选择")
                self.console_output.append("请在最后一个下拉菜单中进行选择")
        else:
            self.result_label.setText("没有可用的选择")
            self.console_output.append("没有可用的选择")

class MGRWRAnalysisPage(QWidget):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("MGRWR 分析")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin: 20px 0;
        """)
        layout.addWidget(title_label)

        analyze_button = ModernButton("开始分析")
        analyze_button.clicked.connect(self.start_analysis)
        layout.addWidget(analyze_button)

    def start_analysis(self):
        # 这里添加 MGRWR 分析的逻辑
        self.console_output.append("开始 MGRWR 分析...")
        # 模拟分析过程
        for i in range(5):
            self.console_output.append(f"分析步骤 {i+1}/5")
        self.console_output.append("MGRWR 分析完成！")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('多功能数据分析工具')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建页面切换按钮
        button_layout = QHBoxLayout()
        self.data_gen_button = ModernButton("数据生成")
        self.dir_select_button = ModernButton("目录选择")
        self.mgrwr_button = ModernButton("MGRWR 分析")

        button_layout.addWidget(self.data_gen_button)
        button_layout.addWidget(self.dir_select_button)
        button_layout.addWidget(self.mgrwr_button)

        main_layout.addLayout(button_layout)

        # 创建堆叠窗口部件
        self.stack = QStackedWidget()
        
        # 创建控制台输出
        self.console_output = ConsoleOutput()

        # 创建三个页面
        self.data_gen_page = DataGenerationPage(self.console_output)
        self.dir_select_page = DirectorySelector(self.console_output)
        self.mgrwr_page = MGRWRAnalysisPage(self.console_output)

        # 将页面添加到堆叠窗口部件
        self.stack.addWidget(self.data_gen_page)
        self.stack.addWidget(self.dir_select_page)
        self.stack.addWidget(self.mgrwr_page)

        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.stack)
        splitter.addWidget(self.console_output)
        splitter.setSizes([400, 200])

        main_layout.addWidget(splitter)

        # 连接按钮信号
        self.data_gen_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.dir_select_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.mgrwr_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
# 重定向 stdout 和 stderr
        sys.stdout = self.console_output
        sys.stderr = self.console_output
    def __del__(self):
        # 恢复 stdout 和 stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())