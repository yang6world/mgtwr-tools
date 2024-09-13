import json
import time
import httpx
import numpy as np
import pandas as pd

index = {}
province_mapping = {
    '北京市': '北京', '天津市': '天津', '上海市': '上海', '重庆市': '重庆', '河北省': '河北', 
    '山西省': '山西', '辽宁省': '辽宁', '吉林省': '吉林', '黑龙江省': '黑龙江', '江苏省': '江苏', 
    '浙江省': '浙江', '安徽省': '安徽', '福建省': '福建', '江西省': '江西', '山东省': '山东', 
    '河南省': '河南', '湖北省': '湖北', '湖南省': '湖南', '广东省': '广东', '海南省': '海南', 
    '四川省': '四川', '贵州省': '贵州', '云南省': '云南', '陕西省': '陕西', '甘肃省': '甘肃', 
    '青海省': '青海', '内蒙古自治区': '内蒙古', '广西壮族自治区': '广西', '西藏自治区': '西藏', 
    '宁夏回族自治区': '宁夏', '新疆维吾尔自治区': '新疆'
}

def get_timestamp():
    return int(time.time() * 1000)


def make_request(params):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://data.stats.gov.cn/easyquery.htm',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest',
    }
    try:
        response = httpx.get('https://data.stats.gov.cn/easyquery.htm', params=params, headers=headers, verify=False,follow_redirects=True,timeout=500)
        response.raise_for_status() 
        return json.loads(response.text)
    except httpx._exceptions.HTTPError as e:
        print(f"Request failed: {e}")
        return None

def get_province_valuecode():
    params = {
        'm': 'getOtherWds',
        'dbcode': 'fsnd',
        'rowcode': 'zb',
        'colcode': 'sj',
        'wds': '[]',
        'k1': get_timestamp(),
    }
    data = make_request(params=params)
    province_code = [item['code'] for item in data['returndata'][0]['nodes']] 
    wds = [{"wdcode":"reg","valuecode":item} for item in province_code]
    return wds

def fetch_data(wds,dfwds):
    params = {
        'm': 'QueryData',
        'dbcode': 'fsnd',
        'rowcode': 'zb',
        'colcode': 'sj',
        'wds': wds,
        'dfwds': dfwds,
        'k1': get_timestamp(),
        'h': '1',
    }
    data = make_request(params=params)
    return data

def process_data(data, province):
    index = [item['cname'] for item in data['returndata']['wdnodes'][0]['nodes']] # Indicators
    columns=[item['cname'] for item in data['returndata']['wdnodes'][2]['nodes']] # Years
    dataset = [item['data']['data'] for item in data['returndata']['datanodes']] # Data
    array=np.array(dataset).reshape(len(index),len(columns))
    
    df = pd.DataFrame(array, columns=columns,index=index)
    df['Province'] = province  # Add the province as a column
    return df


def get_data_pre(data_id, excel_path):
    combined_df = pd.DataFrame() 
    wds = get_province_valuecode()
    for wd in wds:
        print(f"正在获取{wd['valuecode']}的数据...")
        province_code = wd['valuecode']  # Province code
        data = fetch_data(json.dumps([wd]), json.dumps([{"wdcode":"zb","valuecode":data_id},{"wdcode":"sj","valuecode":"LAST20"}]))  # 查询年份参数: LAST5, LAST10, LAST20
        if data:
            province_name = next(item['cname'] for item in data['returndata']['wdnodes'][1]['nodes'] if item['code'] == province_code)
            df = process_data(data, province_name)
            combined_df = pd.concat([combined_df, df], axis=0)  # 添加到总数据集

    combined_df.to_excel(f'pre.xlsx')
    data_pre = pd.read_excel(f'pre.xlsx')
    long_format_data = data_pre.melt(id_vars=['Unnamed: 0', 'Province'], 
                                    var_name='年份', 
                                    value_name='数值')
    # Step 2: 将“指标”列作为列名，通过pivot将其变为宽表
    pivoted_data = long_format_data.pivot_table(index=['Province', '年份'], 
                                                columns='Unnamed: 0', 
                                                values='数值', 
                                                aggfunc='first').reset_index()

    base_data = pd.read_excel(excel_path)
    pivoted_data['Province'] = pivoted_data['Province'].replace(province_mapping)
    # 确保年份只包含数字
    pivoted_data['年份'] = pivoted_data['年份'].str.replace('年', '').astype(int)
    merged_data = pd.merge(base_data, pivoted_data, left_on=['省份', '年份'], right_on=['Province', '年份'], how='left')
    # 删除多余的列
    merged_data = merged_data.drop(columns=['Province'])
    merged_data.to_excel(excel_path, index=False)
    print(f'数据已保存至{excel_path}')
    return True