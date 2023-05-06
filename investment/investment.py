import pandas as pd

df = pd.read_csv('investment.csv')

df['global'] = df['global'].cumsum()
df['chinese'] = df['chinese'].cumsum()

df.to_csv('investment-group-cum.csv', index=False)
