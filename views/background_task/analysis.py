import sys
from multiprocessing import Queue

from utils.data_analysis import DataAnalysis


class QueueWriter:
    """将子进程的 print 输出重定向到 multiprocessing.Queue 的类。"""

    def __init__(self, queue):
        self.queue = queue

    def write(self, message):
        # 直接将 message 放入队列，保留换行符等特殊字符
        self.queue.put(message)

    def flush(self):
        """flush 方法可以留空或传递，因为 queue 本身是无缓冲的。"""
        pass


def analysis_process(file_path, output_path, y_var, x_vars, coords, t_var, kernel, fixed, criterion, model, params,
                     queue):
    """
    分析任务进程，实际执行分析并通过队列报告状态。
    queue: 用于传递子进程的状态和 print 输出
    """
    try:
        # 重定向 sys.stdout 到队列
        sys.stdout = QueueWriter(queue)
        sys.stderr = QueueWriter(queue)
        print(f"开始 {model} 分析...")
        # 模拟分析任务
        analysis = DataAnalysis(file_path, output_path)
        analysis.set_variables(x_vars, [y_var], [t_var], coords)

        if model == 'GTWR':
            bw_min, bw_max, tau_min, tau_max, tol, bw_decimal, tau_decimal, max_iter = params['bw_min'], params[
                'bw_max'], params['tau_min'], params['tau_max'], params['tol'], params['bw_decimal'], params[
                'tau_decimal'], params['max_iter']
            analysis.gtwr(kernel=kernel, fixed=fixed, criterion=criterion,
                          bw_min=bw_min, bw_max=bw_max, tau_min=tau_min, tau_max=tau_max, tol=tol,
                          bw_decimal=bw_decimal, tau_decimal=tau_decimal, max_iter=max_iter)
        elif model == 'MGTWR':
            bw_min_input, bw_max_input, tau_min_input, tau_max_input, multi_bw_min_input, multi_bw_max_input, multi_tau_min_input, multi_tau_max_input, tol_input, bw_decimal_input, tau_decimal_input, init_bw_input, init_tau_input, tol_multi_input, rss_score_input = \
                params['bw_min'], params['bw_max'], params['tau_min'], params['tau_max'], params['multi_bw_min'], \
                    params['multi_bw_max'], params['multi_tau_min'], params['multi_tau_max'], params['tol'], params[
                    'bw_decimal'], params['tau_decimal'], params['init_bw'], params['init_tau'], params['tol_multi'], \
                    params['rss_score']

            analysis.mgtwr(kernel=kernel, fixed=fixed, criterion=criterion,
                           bw_min=bw_min_input, bw_max=bw_max_input, tau_min=tau_min_input, tau_max=tau_max_input,
                           multi_bw_min=multi_bw_min_input, multi_bw_max=multi_bw_max_input,
                           multi_tau_min=multi_tau_min_input, multi_tau_max=multi_tau_max_input, tol=tol_input,
                           bw_decimal=bw_decimal_input, tau_decimal=tau_decimal_input, init_bw=init_bw_input,
                           init_tau=init_tau_input, tol_multi=tol_multi_input, rss_score=rss_score_input)

        print(f"{model} 分析完成")
    except Exception as e:
        print(f"分析错误: {e}")
    finally:
        sys.stdout = sys.__stdout__  # 恢复标准输出
        sys.stderr = sys.__stderr__
