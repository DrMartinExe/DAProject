import pandas as pd

# Read the data into a new dataframe
df = pd.read_csv("Coffee_company.csv")
print(df.head())
print(df.columns)

# Clean up the column headings
print(df.columns.str.strip())
print(df.head())
print(df.columns)


