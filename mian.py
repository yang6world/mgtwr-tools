import pandas as pd
from mgtwr.sel import SearchMGTWRParameter
from mgtwr.model import MGTWR

data = pd.read_excel('pivoted_data.xlsx')
coords = data[['经度', '纬度']]
t = data[['年份']]
# 自变量
X = data[['全体居民人均可支配收入']]
# 因变量
y = data[['重力值']]
# 带宽选择
selector = SearchMGTWRParameter(coords, t, X, y, kernel='gaussian', fixed=True)
bws = selector.search(multi_bw_min=[0.1], verbose=True, tol_multi=1.0e-4, time_cost=True)
print("Selected bandwidths:", bws)
# 拟合MGTWR模型
mgtwr_model = MGTWR(coords, t, X, y, selector, kernel='gaussian', fixed=True)
mgtwr_results = mgtwr_model.fit(n_jobs=200)

print("R-squared value:", mgtwr_results.R2)
print("aic value:", mgtwr_results.aic)
print("aicc value:", mgtwr_results.aic_c)
print("bic value:", mgtwr_results.bic)
print("ENP value:", mgtwr_results.ENP)
print("tr_S value:", mgtwr_results.tr_S)
print("adj_R2 value:", mgtwr_results.adj_R2)
print("RSS value:", mgtwr_results.RSS)
print("df_model value:", mgtwr_results.df_model)
print("sigma2 value:", mgtwr_results.sigma2)
print("betas value:", mgtwr_results.betas)
# 可视化



