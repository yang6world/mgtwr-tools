import pandas as pd
from mgtwr.model import GTWR, MGTWR, GTWRResults
from mgtwr.sel import SearchGTWRParameter
from mgtwr.model import GTWR
from mgtwr.sel import SearchMGTWRParameter
from mgtwr.model import MGTWR


class DataAnalysis:
    def __init__(self, input_path, output_path):
        self.file_path = input_path
        self.excel_data = self.get_xlsx_data(input_path)
        self.output_path = output_path
        self.x = None
        self.y = None
        self.t = None
        self.coords = None

    @staticmethod
    def get_xlsx_data(path):
        """
        获取数据
        :param path: 文件路径
        :return:
        """
        data = pd.read_excel(path)
        return data

    def get_headers(self):
        """
        获取表头
        """
        return self.excel_data.columns.tolist()

    # 获取自变量,因变量, 时间变量, 坐标变量
    def set_variables(self, x: list, y: list, t: list, coords: list):
        """
        设置自变量:x,因变量:y, 时间变量:t, 坐标变量:coords
        """
        self.x = self.excel_data[x]
        self.y = self.excel_data[y]
        self.t = self.excel_data[t]
        self.coords = self.excel_data[coords]
        print("自变量:", self.x)
        print("因变量:", self.y)
        print("时间变量:", self.t)
        print("坐标变量:", self.coords)

    def gtwr(self, kernel: str,
             fixed: bool,
             criterion: str = 'AICc',
             bw_min: float = None,
             bw_max: float = None,
             tau_min: float = None,
             tau_max: float = None,
             tol: float = 1.0e-6,
             bw_decimal: int = 1,
             tau_decimal: int = 1,
             max_iter: int = 200, ):
        """
        选择GTWR模型的一个唯一带宽和时空尺度的方法。

        参数
        ----------
        kernel         : string
                         使用的核函数类型，用于加权观测值；
                         可用选项：
                         'gaussian'（高斯核）
                         'bisquare'（双平方核）
                         'exponential'（指数核）
        fixed          : bool
                         True表示基于距离的核函数（默认），False表示自适应（基于最近邻）的核函数
        criterion      : string
                         带宽选择准则：'AICc'（修正赤池信息准则）、'AIC'（赤池信息准则）、'BIC'（贝叶斯信息准则）、'CV'（交叉验证）
        bw_min         : float
                         带宽搜索的最小值
        bw_max         : float
                         带宽搜索的最大值
        tau_min        : float
                         时空尺度搜索的最小值
        tau_max        : float
                         时空尺度搜索的最大值
        tol            : float
                         确定收敛所使用的容差
        max_iter       : integer
                         如果没有达到收敛，则最大迭代次数
        bw_decimal     : scalar
                         带宽搜索时保存的小数位数
        tau_decimal    : scalar
                         时空尺度搜索时保存的小数位数
        """
        # 输出传入的参数
        for key, value in locals().items():
            if key != 'self':
                print(f"{key}: {value}")
        # 带宽选择
        sel = SearchGTWRParameter(self.coords, self.t, self.x, self.y, kernel=kernel, fixed=fixed)
        bw, tau = sel.search(verbose=True, time_cost=True, criterion=criterion, bw_min=bw_min, bw_max=bw_max,
                             tau_min=tau_min, tau_max=tau_max, tol=tol, max_iter=max_iter, bw_decimal=bw_decimal,
                             tau_decimal=tau_decimal)
        gtwr = GTWR(self.coords, self.t, self.x, self.y, bw, tau, kernel=kernel, fixed=fixed).fit()
        print(gtwr.R2)

        print("R平方值:", gtwr.R2)
        print("AIC值:", gtwr.aic)
        print("AICc值:", gtwr.aicc)
        print("BIC值:", gtwr.bic)
        print("有效参数数 (ENP) 值:", gtwr.ENP)
        print("迹 (tr_S) 值:", gtwr.tr_S)
        print("调整后的R平方值:", gtwr.adj_R2)
        print("残差平方和 (RSS) 值:", gtwr.RSS)
        print("模型自由度 (df_model) 值:", gtwr.df_model)
        print("sigma2值:", gtwr.sigma2)
        print("回归系数 (betas) 值:", gtwr.betas)
        self.output_betas(gtwr.betas)


    def mgtwr(self, kernel: str,
              fixed: bool,
              criterion: str = 'AICc',
              bw_min: float = None,
              bw_max: float = None,
              tau_min: float = None,
              tau_max: float = None,
              tol: float = 1.0e-6,
              bw_decimal: int = 1,
              tau_decimal: int = 1,
              init_bw: float = None,
              init_tau: float = None,
              multi_bw_min: list = None,
              multi_bw_max: list = None,
              multi_tau_min: list = None,
              multi_tau_max: list = None,
              tol_multi: float = 1.0e-5,
              rss_score: bool = False,
              ):
        """
        为GTWR模型选择唯一带宽和时空尺度，或为MGTWR模型选择带宽向量和时空尺度向量的方法。

        参数
        ----------
        kernel          : string
                          核函数类型，用于加权观测值；
                          可用选项：
                          'gaussian'（高斯核）
                          'bisquare'（双平方核）
                          'exponential'（指数核）

        fixed           : bool
                          True表示基于距离的核函数，False表示自适应（基于最近邻）的核函数（默认）

        criterion       : string
                          带宽选择准则：'AICc'（修正赤池信息准则）、'AIC'（赤池信息准则）、'BIC'（贝叶斯信息准则）、'CV'（交叉验证）

        bw_min          : float
                          带宽搜索的最小值

        bw_max          : float
                          带宽搜索的最大值

        tau_min         : float
                          时空尺度搜索的最小值

        tau_max         : float
                          时空尺度搜索的最大值

        multi_bw_min    : list
                          在MGTWR带宽搜索中，每个协变量的最小值。可以是单个值，也可以为每个协变量（包括截距）提供一个值

        multi_bw_max    : list
                          在MGTWR带宽搜索中，每个协变量的最大值。可以是单个值，也可以为每个协变量（包括截距）提供一个值

        multi_tau_min   : list
                          在MGTWR时空尺度搜索中，每个协变量的最小值。可以是单个值，也可以为每个协变量（包括截距）提供一个值

        multi_tau_max   : list
                          在MGTWR时空尺度搜索中，每个协变量的最大值。可以是单个值，也可以为每个协变量（包括截距）提供一个值

        tol             : float
                          确定收敛所使用的容差

        bw_decimal      : int
                          带宽搜索时保留的小数位数

        tau_decimal     : int
                          时空尺度搜索时保留的小数位数

        init_bw         : float
                          初始化MGTWR时使用的带宽，默认从GTWR派生，否则可以手动指定

        init_tau        : float
                          初始化MGTWR时使用的时空尺度，默认从GTWR派生，否则可以手动指定

        tol_multi       : float
                          多带宽回归算法的收敛容差；较大的容差可能会加快算法停止，但可能会导致次优模型

        rss_score      : bool
                         如果为 True，则在每次多带宽回归算法的迭代中使用残差平方和（RSS）来评估结果；
                         如果为 False，则使用一个平滑函数来进行评估；默认值为 False。

    """
        for key, value in locals().items():
            if key != 'self':
                print(f"{key}: {value}")
        selector = SearchMGTWRParameter(self.coords, self.t, self.x, self.y, kernel=kernel, fixed=fixed)
        bws = selector.search(verbose=True, time_cost=True, criterion=criterion, bw_min=bw_min, bw_max=bw_max,
                              tau_min=tau_min, tau_max=tau_max, tol=tol, bw_decimal=bw_decimal, tau_decimal=tau_decimal,
                              init_bw=init_bw, init_tau=init_tau, multi_bw_min=multi_bw_min, multi_bw_max=multi_bw_max,
                              multi_tau_min=multi_tau_min, multi_tau_max=multi_tau_max, tol_multi=tol_multi,
                              rss_score=rss_score)
        print("选择的带宽:", bws)
        # 拟合MGTWR模型
        mgtwr_model = MGTWR(self.coords, self.t, self.x, self.y, selector, kernel=kernel, fixed=fixed)
        mgtwr_results = mgtwr_model.fit()

        # 输出结果
        print("R平方值:", mgtwr_results.R2)
        print("AIC值:", mgtwr_results.aic)
        print("AICc值:", mgtwr_results.aic_c)
        print("BIC值:", mgtwr_results.bic)
        print("有效参数数 (ENP) 值:", mgtwr_results.ENP)
        print("迹 (tr_S) 值:", mgtwr_results.tr_S)
        print("调整后的R平方值:", mgtwr_results.adj_R2)
        print("残差平方和 (RSS) 值:", mgtwr_results.RSS)
        print("模型自由度 (df_model) 值:", mgtwr_results.df_model)
        print("sigma2值:", mgtwr_results.sigma2)
        print("回归系数 (betas) 值:", mgtwr_results.betas)
        self.output_betas(mgtwr_results.betas)

    # 输出回归系数的xlsx
    def output_betas(self, betas):
        """
        输出回归系数到xlsx文件，包含自变量名称，并将经纬度和年份信息也添加到表中。
        :param betas: 回归系数矩阵
        """
        # 从 self.x 的列名中获取自变量名称
        variable_names = ['Intercept'] + self.x.columns.tolist()
        # 创建 DataFrame 并设置表头
        df_betas = pd.DataFrame(betas, columns=variable_names)
        # 添加经纬度和年份信息
        df_betas['Longitude'] = self.coords.iloc[:, 1]  # 经度
        df_betas['Latitude'] = self.coords.iloc[:, 0]  # 纬度
        df_betas['Year'] = self.t  # 年份

        # 输出到 Excel 文件
        df_betas.to_excel(self.output_path, index=False)
        print(f"回归系数表输出至 {self.output_path}")

