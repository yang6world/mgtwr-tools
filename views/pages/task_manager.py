import psutil
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QMainWindow
from PyQt5.QtCore import QTimer, QThread
from multiprocessing import Process, Manager


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tasks = {}  # 使用字典来存储任务ID和对应的线程或进程对象
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_resources)
        self.timer.start(1000)  # 每秒刷新一次任务资源使用情况

    def initUI(self):
        self.setWindowTitle("任务管理器")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # 创建任务列表表格
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["任务ID", "状态", "类型", "CPU%", "内存(MB)"])
        layout.addWidget(self.task_table)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.terminate_task_button = QPushButton("终止任务")
        button_layout.addWidget(self.terminate_task_button)
        layout.addLayout(button_layout)

        # 终止任务按钮点击事件
        self.terminate_task_button.clicked.connect(self.terminate_task)

        # 主窗口布局
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_task(self, task_id, task, task_type):
        """
        task_type: "线程" 或 "进程" 标识任务的类型
        """
        # 将新任务添加到表格和任务管理器
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)
        self.task_table.setItem(row_position, 0, QTableWidgetItem(str(task_id)))
        self.task_table.setItem(row_position, 1, QTableWidgetItem("运行中"))
        self.task_table.setItem(row_position, 2, QTableWidgetItem(task_type))  # 显示任务是线程还是进程
        self.task_table.setItem(row_position, 3, QTableWidgetItem("0"))  # 初始CPU%
        self.task_table.setItem(row_position, 4, QTableWidgetItem("0"))  # 初始内存MB

        # 将任务存储到字典中
        self.tasks[task_id] = {'task': task, 'type': task_type}

    def terminate_task(self):
        """
        根据任务的类型，终止任务。
        """
        # 获取选中的任务并终止它
        row = self.task_table.currentRow()
        if row == -1:
            return  # 没有选中任务

        task_id = int(self.task_table.item(row, 0).text())
        task_info = self.tasks.get(task_id)

        if task_info:
            task = task_info['task']
            task_type = task_info['type']

            if task_type == "线程" and isinstance(task, QThread):
                task.stop()  # 调用线程的停止方法
                self.task_table.setItem(row, 1, QTableWidgetItem("已终止"))

            elif task_type == "进程" and isinstance(task, Process):
                task.terminate()  # 终止进程
                task.join()  # 等待进程终止
                self.task_table.setItem(row, 1, QTableWidgetItem("已终止"))

    def refresh_resources(self):
        """
        刷新每个任务的资源使用情况
        """
        for task_id, task_info in self.tasks.items():
            task = task_info['task']
            task_type = task_info['type']

            # 检查任务是进程并且任务仍在运行
            if task_type == "进程" and isinstance(task, Process) and task.is_alive():
                try:
                    # 使用 psutil 获取该进程的资源占用情况
                    process = psutil.Process(task.pid)  # 获取进程 ID
                    cpu_usage = process.cpu_percent(interval=1) / psutil.cpu_count()
                    memory_usage = process.memory_info().rss / (1024 * 1024)  # 转换为MB

                    # 更新表格中任务的资源占用情况
                    for i in range(self.task_table.rowCount()):
                        if int(self.task_table.item(i, 0).text()) == task_id:
                            self.task_table.setItem(i, 3, QTableWidgetItem(f"{cpu_usage:.2f}"))
                            self.task_table.setItem(i, 4, QTableWidgetItem(f"{memory_usage:.2f}"))
                except psutil.NoSuchProcess:
                    continue

    def delete_task(self, task_id):
        # 删除任务
        for i in range(self.task_table.rowCount()):
            if int(self.task_table.item(i, 0).text()) == task_id:
                self.task_table.removeRow(i)
                break
        del self.tasks[task_id]
