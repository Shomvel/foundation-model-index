import pandas as pd

df = pd.read_csv('filtered_arxiv_data.csv')
# Calculate the total number of rows in the DataFrame
total_rows = df.shape[0]

# Count the number of rows with a valid doi
valid_doi_count = df[df['doi'].notnull()].shape[0]

# Calculate the proportion of rows with valid doi
proportion = valid_doi_count / total_rows

print(total_rows)
print(f"Proportion of rows with valid doi: {proportion:.2%}")
