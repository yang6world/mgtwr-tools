import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 读取Excel文件中的数据
file_path = '/mnt/data/data.xlsx'
data = pd.read_excel(file_path)


def calculate_vif(data: pd.DataFrame, columns: list):
    variables = data[columns]
    # 为了计算VIF，在模型中添加常数项
    X = np.column_stack([np.ones(variables.shape[0]), variables])
    # 计算每个变量的VIF值
    vif_data = pd.DataFrame()
    vif_data["Feature"] = ['const'] + list(variables.columns)
    vif_data["VIF"] = [variance_inflation_factor(X, i) for i in range(X.shape[1])]

    # 显示VIF结果
    print(vif_data)



