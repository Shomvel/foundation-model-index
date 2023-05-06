import pandas as pd

# 读取 CSV 文件并将其转换为 DataFrame
df1 = pd.read_csv('app-chinese.csv')
df2 = pd.read_csv('app_global_index.csv')

# 将 date 列转换为日期时间格式
df1['date'] = pd.to_datetime(df1['date'])
df2['date'] = pd.to_datetime(df2['date'])

# 合并两个 DataFrame
merged_df = pd.merge(df1, df2, on='date')


# 将结果保存到 CSV 文件
merged_df.to_csv('apps-cumsum.csv', index=False)