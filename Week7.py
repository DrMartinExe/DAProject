##############
# Week 7 Code

# import the libraries
import pandas as pd
import matplotlib.pyplot as plt

# Read the data into a new dataframe
df = pd.read_csv("Coffee_company.csv")
print(df.head())
print(df.columns)

# Clean up the column headings
df.columns = df.columns.str.strip()
print(df.head())
print(df.columns)

# Round up 'Units Sold' data by converting it to int
df['Units Sold'] = df['Units Sold'].astype(int)
print(df.head())

# Change 'Month Name' to 'Month" 
# If we didn't strip the column names this would not work

print(df.columns) # to check the exact name of each column
df.rename(columns={'Month Name':'Month'}, inplace = True)
print(df.head())
print(df.columns)

# 
# 
# Week 7 Extension Code
# Calculate total Sales

df['Sales'] = pd.to_numeric(df['Sales'].str.replace(',', '').str.replace('$', ''), errors='coerce')
#df['Sales'] = pd.to_numeric(df['Sales'].str.replace(',', '', regex=False).str.replace('$', '', regex=False), errors='coerce')
df['Sales'] = df['Sales'].astype(float)
total_sales = df['Sales'].sum()
print("Total Sales: $", total_sales)


# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Calculate quarterly sales
quarterly_sales = df['Sales'].resample('Q').sum().reset_index()
quarterly_sales.columns = ['Quarter', 'Total Sales']

print(quarterly_sales)
