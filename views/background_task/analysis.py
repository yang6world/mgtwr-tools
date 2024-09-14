import time
from multiprocessing import Process, Manager


class WorkerProcess:
    """封装分析任务的进程"""

    def __init__(self, task_id, update_func):
        self.task_id = task_id
        self.update_func = update_func
        self.manager = Manager()
        self.result_dict = self.manager.dict()
        self.result_dict['status'] = "初始化中"
        self.process = Process(target=self.run_task)

    def run_task(self):
        """模拟耗时任务"""
        for i in range(10):
            time.sleep(1)
            self.result_dict['status'] = f"任务 {self.task_id} 进度: {i + 1}/10"
            self.update_func(self.result_dict['status'])

        self.result_dict['status'] = f"任务 {self.task_id} 完成"
        self.update_func(self.result_dict['status'])

    def start(self):
        """启动任务"""
        self.process.start()

    def terminate(self):
        """终止任务"""
        if self.process.is_alive():
            self.process.terminate()
            self.process.join()
            self.update_func(f"任务 {self.task_id} 已终止")
