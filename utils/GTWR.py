import pandas as pd
from mgtwr.model import GTWR, MGTWR,GTWRResults
from mgtwr.sel import SearchGTWRParameter
from mgtwr.model import GTWR

data = pd.read_excel('pivoted_data.xlsx')
coords = data[['经度', '纬度']]
t = data[['年份']]
# 自变量
X = data[['全体居民人均可支配收入']]
# 因变量
y = data[['重力值']]
print(y)
print(X)
# 带宽选择
sel = SearchGTWRParameter(coords, t, X, y, kernel='gaussian', fixed=True)
bw, tau = sel.search(tau_max=20, verbose=True, time_cost=True)
gtwr = GTWR(coords, t, X, y, bw, tau, kernel='gaussian', fixed=True).fit()
print(gtwr.R2)

print("R-squared value:", gtwr.R2)
print("aic value:", gtwr.aic)
print("aicc value:", gtwr.aic_c)
print("bic value:", gtwr.bic)
print("ENP value:", gtwr.ENP)
print("tr_S value:", gtwr.tr_S)
print("adj_R2 value:", gtwr.adj_R2)
print("RSS value:", gtwr.RSS)
print("df_model value:", gtwr.df_model)
print("sigma2 value:", gtwr.sigma2)
print("betas value:", gtwr.betas)
# 可视化



