import pandas as pd

# 读取 CSV 文件并将其转换为 DataFrame
df = pd.read_csv('filtered_arxiv_data.csv')

# 指定的关键词列表
keywords = ['Foundation Model', 'Multimodal', 'large language model',
            'Foundation Language Model', 'foundation vision', 'Vicuna', 'LLaMA', 'GPT', 'RLHF']

# 在 title 和 abstract 列中查找指定的关键词
mask = df['title'].str.contains('|'.join(keywords), case=False) | \
       df['abstract'].str.contains('|'.join(keywords), case=False)

# 如果 title 或 abstract 中包含关键词，则将 is_large_model 列设置为 True
df.loc[mask, 'is_large_model'] = True

# 将 time 列转换为日期时间格式
df['time'] = pd.to_datetime(df['time'])

# 按周分组并统计每个组中的 is_large_model 列的 True 值数量，并计算累积和
grouped = df.groupby(pd.Grouper(key='time', freq='W-MON'))['is_large_model'].sum().cumsum()

df['is_chinese_large_model'] = df['is_chinese'] & df['is_large_model']
# 将 DataFrame 按周分组，并统计每个组中 is_chinese_large_model 列为 True 的数量，并计算累积和
chinese_grouped = df.groupby([pd.Grouper(key='time', freq='W-MON')])['is_chinese_large_model'].sum().cumsum()

# 将 grouped 和 chinese_grouped 拼接到一起
result = pd.concat([grouped, chinese_grouped], axis=1)
result.columns = ['global_large_model_papers', 'chinese_large_model_papers']

# 将结果保存到 CSV 文件
result.to_csv('./data/large-model-papers.csv')
