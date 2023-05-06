import pandas as pd
import re

# 加载CSV文件
data = pd.read_csv('大模型创新指数 - 大模型应用指数.csv')

# 将字符串格式的日期转换为 datetime 对象
data['date'] = pd.to_datetime(data['date'], format='%m/%d/%Y')

# 筛选指定日期范围内的数据
start_date = '2022-12-01'
end_date = '2023-05-05'
mask = (data['date'] >= start_date) & (data['date'] <= end_date)
filtered_data = data.loc[mask]

# 使用 Grouper 按周分组并计算累积和
grouped_data = filtered_data.groupby(pd.Grouper(key='date', freq='W-MON')).size().cumsum()

# 将结果保存到CSV文件
grouped_data.to_csv('pivot-weekly.csv', index=True, header=['projects'])

# 定义一个函数，检查字符串中是否含有中文字符
def contains_chinese(s):
    return bool(re.search('[\u4e00-\u9fff]', s))

# 筛选出 'global' 字段中含有中文字符的项目
data_with_chinese = filtered_data[filtered_data['global'].apply(contains_chinese)]

grouped_data_chinese = data_with_chinese.groupby(pd.Grouper(key='date', freq='W-MON')).size().cumsum()

# 保存并显示结果
grouped_data_chinese.to_csv('pivot-weekly-chinese.csv', index=True, header=['projects'])
