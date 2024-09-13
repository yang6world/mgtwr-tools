from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker

from utils.reptile import get_data_pre


class AnalysisThread(QThread):
    progress_signal = pyqtSignal(str)  # 任务进度信号
    finished_signal = pyqtSignal(str)  # 任务完成信号
    error_signal = pyqtSignal(str)  # 任务错误信号
    resource_signal = pyqtSignal(dict)  # 任务资源监控信号

    def __init__(self, selected_id, filepath, task_id):
        super().__init__()
        self.selected_id = selected_id
        self.filepath = filepath
        self.task_id = task_id  # 任务唯一标识
        self.running = True  # 任务是否正在运行
        self.mutex = QMutex()  # 用于线程安全的互斥锁

    def run(self):
        self.progress_signal.emit(f"开始进行数据分析，任务ID: {self.task_id}")
        try:
            if not self.running:
                return  # 检查任务是否被终止
            get_data_pre(self.selected_id, self.filepath)
            self.finished_signal.emit(f"分析完成，任务ID: {self.task_id}")
        except Exception as e:
            self.error_signal.emit(f"错误: {e}")

    def stop(self):
        with QMutexLocker(self.mutex):
            self.running = False
        self.finished_signal.emit(f"任务已终止，任务ID: {self.task_id}")



