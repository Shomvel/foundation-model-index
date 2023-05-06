import pandas as pd

# 读取csv文件
df = pd.read_csv('dylan-products.csv')

# 筛选出url字段中包含'.cn'或者name中包含中文的数据
mask = df['url'].str.contains('.cn') | df['name'].str.contains('[\u4e00-\u9fa5]+')
filtered_df = df[mask]

# 转换日期格式，并按周分组
filtered_df['launched_at'] = pd.to_datetime(filtered_df['launched_at'])


start_date = "2022-12-01"
end_date = "2023-05-31"
filtered_df = filtered_df.query("@start_date <= launched_at <= @end_date")

grouped_df = filtered_df.groupby(pd.Grouper(key='launched_at', freq='W-MON'))['name'].count().cumsum()
# 输出结果
grouped_df.to_csv('app-chinese.csv')
