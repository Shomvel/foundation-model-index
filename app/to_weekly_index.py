import pandas as pd

df1 = pd.read_csv('data/futurepedia.csv')
df2 = pd.read_csv('data/phygital.csv')

# 假设有两个DataFrame：df1和df2
combined_df = pd.concat([df1, df2]).drop_duplicates(subset="name", keep="first").reset_index(drop=True)
print(len(df1), len(df2), len(df1) + len(df2), len(combined_df))
combined_df.to_csv('total.csv')

combined_df["date"] = pd.to_datetime(combined_df["date"])
combined_df["date"] = combined_df["date"].dt.tz_localize(None)

start_date = "2022-12-01"
end_date = "2023-05-31"
combined_df = combined_df.query("@start_date <= date <= @end_date")

# 按周分组数据
combined_df["week"] = combined_df["date"].dt.to_period("W")

# 对每个组进行聚合，以获得每周的产品列表
grouped = combined_df.groupby([pd.Grouper(key='date', freq='W-MON')]).size().cumsum()
grouped.to_csv('./data/app_global_index.csv')
